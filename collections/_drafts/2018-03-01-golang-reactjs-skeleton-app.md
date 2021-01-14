# An example modern web-app architecture with ReactJS and Golang
At a recent Atlassian internship I was introduced to [Golang](https://golang.org/) and quite enjoyed it. I used it in the context of a web application backend that supported a [ReactJS](https://reactjs.org/) frontend.  I found the combination to be enjoyable, so I’ve built a small skeleton app (*another* ‘todo app’) for future use bootstrapping web app projects. It follows modern web-app best practices, attempting particularly  to follow the [12-Factor methodology](https://12factor.net/). Let’s run through it. 

> **NOTE:** The full code is available at https://github.com/thundergolfer/golang-reactjs-skeleton-app

### Overall Structure 

Our ReactJS web app front-end is stored in `frontend/`. The `.js` gets bundled with [Webpack](https://webpack.js.org/) into a file, `bundle.js`, which in then packaged into our Golang web-backend along with an `index.html` and CSS static files, and served whenever a visitor hits the `/` root route.

The Golang backend web app is basically an API connected to a datastore, all code for which is in `backend/`. In the simplest case, our datastore is in-memory, but the app also has code to use [Google Cloud Datastore](https://cloud.google.com/datastore/docs/concepts/overview) (Google’s ‘S3’) as a persistent datastore. 

Following the 12-Factor methodology, all application config that varies by environment context (ie. dev, staging, prod) is kept in the environment variable space. 

### Setting up the Golang backend API

```
package main

import (
	"net/http"
	log "github.com/sirupsen/logrus"
)

func main() {
	port := "8080"
	router := NewRouter()

	log.Fatal(http.ListenAndServe(":"+port, router))
}
```

This is, `backend/main.go`  the entry point for our backend. All it does is create a router and give it to the Golang [`http`](https://golang.org/pkg/net/http/) package’s  [`ListenAndServe(addr string, handle Handler)`](https://golang.org/pkg/net/http/#ListenAndServe) method which will start a web server for us. 

The obviously interesting and important bit is the `router`, so let’s check out `backend/router.go`. 

#### The Web Server Router -  `backend/router.go`

```
package main

import (
	"net/http"
	"github.com/gorilla/mux"
)

func NewRouter() *mux.Router {
	router := mux.NewRouter()

	setupStatic(router)
	config := newConfig()
	app := newApp(config)

	routes := routes(app)
	for _, route := range routes {
		var handler http.Handler

		handler = route.HandlerFunc
		handler = Logger(handler, route.Name)

	router.Methods(route.Method).Path(route.Pattern).Name(route.Name).Handler(handler)
	}

	return router
}
```

We can see the `NewRouter()` function here that created our `router` structure. It first create the `gorilla/mux` libraries router, which will match incoming HTTP requests to particular ‘handler’ functions based on request characteristics like path and HTTP type (eg. POST). For reasons to use Gorilla’s router rather than the standard Golang one see [here](http://www.gorillatoolkit.org/pkg/mux) . 

We then call `setupStatic(router)`, which will allow our backend to serve `.html`, `.js`, and `.css` static files like our `index.html`, but I’ll get back to that later. 

Then a `config` structure is created, which picks up application configuration from the environment. That logic is in `backend/config.go` and just looks like this. 

```
package main

import "os"

type config struct {
	datastoreType                string
	projectID                    string
	googleCloudStorageBucketName string
}

func newConfig() config {
	c := config{}
	c.datastoreType = getEnv("DATASTORE", "local")
	c.projectID = getEnv("PROJECT_ID", "twelve-factor-app")
	c.googleCloudStorageBucketName = getEnv("GOOGLE_CLOUD_BUCKET_NAME", "")
	return c
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}
``` 

Now we pass our `config` into a `newApp()` function. What does that function give us? It gives an `App` struct, which in this simple todo app just holds a reference to a `datastore` and has attached to it all our ‘handler’ functions. The `datastore` is an interface which offers us handling typical CRUD creation, deletion and retrieval.  We’ll explore it further later. 

We’re now here, with an initialised `config` and an `app` that has only a `datastore` reference:

```
routes := routes(app)
```

Remember  how our router just matches HTTP requests to ‘handler’ functions? Well the `routes` function is what constructs our list of request patterns to match against, and which particular ‘handler’ function of the app is to be invoked when the pattern is matched. Here’s `backend/routes.go`:

```
package main

import "net/http"

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

func routes(app *App) Routes {
	var routes = Routes{
		Route{
			"Index",
			"GET",
			"/",
			app.Index,
		},
		Route{
			"TodoIndex",
			"GET",
			"/api/todos",
			app.TodoIndex,
		},
		Route{
			"TodoCreate",
			"POST",
			"/api/todos",
			app.TodoCreate,
		},
		Route{
			"TodoShow",
			"GET",
			"/api/todos/{todoId}",
			app.TodoShow,
		},
		Route{
			"TodoDelete",
			"DELETE",
			"/api/todos/{todoId}",
			app.TodoDelete,
		},
	}
	return routes
}
```

Let’s look at one particular `Route` structure, which defined a request pattern and a ‘handler’ to associate with it. 

```
Route{
	"TodoShow",
	"GET",
	"/api/todos/{todoId}",
	app.TodoShow,
},
```

The first field is just a helpful name for log output. The 2nd, `”GET"`, is the [HTTP Method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods), and the 3rd field is the path pattern, which in this case matches `/api/todos/` exactly and then some following variable string which will get stored as `todoId`. The 4th field is our handler, the method `TodoShow` attached to our `app` structure. Basically when a user hits `/api/todos/100` we will show them the todo object with id=100.  If you’re wondering what exact a ‘handler’ function looks like, we’ll be getting to that after we’ve attached our routes to the router.

After getting our `routes` list back from `routes(app)` we’re going to attach them to our `gorilla/mux` router, which is what this block back in `router.go` does:

```
	for _, route := range routes {
		var handler http.Handler

		handler = route.HandlerFunc
		handler = Logger(handler, route.Name)

		router.Methods(route.Method).Path(route.Pattern).Name(route.Name).Handler(handler)
	}
```

We’re looping over each `Route` and first wrapping its `HandlerFunc`  in a ` Logger`, which will nicely format some logs to `stdout` to record that the request happened in our app. That code is, logically, in `backend/logger.go`. Then we pull out all the rest of the pieces of our app and pass them into the method chaining API of the `gorilla/mux` router, which is quite readable. 

And we’re done! The router is returned ready to handle all our api requests. There’s three things we touched but didn’t explore that we’ll now go back to: 

* The static file route handling (key to serving our frontend JS)
* The ‘handler’ functions 
* The `datastore` interface (key to abstracting the storage mechanism of our todos from application logic)

We’ll now explore these in turn. 

#### Static file Routing - `backend/router.go`

Here is the `setupStatic` method again. 

```
func setupStatic(router *mux.Router) {
	var handler http.HandlerFunc
	handler = StaticHandler
	router.PathPrefix("/public/").Handler(Logger(handler, "/public/"))
	router.PathPrefix("/static/").Handler(Logger(handler, "/static/"))
}
```

There’s a bit of weirdness where we defined a variable that is of the interface type `http.HandlerFunc` and then assigned our `StaticHandler` ‘handler’ function to it. This is because the `StaticHandler` function in `backend/handlers.go` has the function signature `func(w http.ResponseWriter, r *http.Request)`, but the router only accepts the interface `http.HandlerFunc`. Fortunately, any function with that  signature satisfies the `http.HandlerFunc` interface, and so we are allowed to our concrete function implementation to the variable of that interface type. Read [this blog post](http://www.alexedwards.net/blog/a-recap-of-request-handling) to go more in depth on it. 

After wrapping our handler with the `Logger`  we assign the functions with `PathPrefix`. This means that any request with a path that has a *prefix* of either “/public/” or “/static/“ will invoke the `StaticHandler`. This allows paths like `/public/index.html` and `/static/js/bundles.js` to work. 

#### The ‘Handler` functions

All ‘handler’ functions are in `backend/handlers.go`, and they are all attached as methods on the `App` structure, so that they can access the `datastore`. Let’s look at the function that creates a todo in our `datastore`. 

```
func (app *App) TodoCreate(w http.ResponseWriter, r *http.Request) {
	var todo types.Todo
	body, err := ioutil.ReadAll(io.LimitReader(r.Body, 1048576))
	if err != nil {
		panic(err)
	}
	if err := r.Body.Close(); err != nil {
		panic(err)
	}
	if err := json.Unmarshal(body, &todo); err != nil {
		w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		w.WriteHeader(422) // unprocessable entity
		if err := json.NewEncoder(w).Encode(err); err != nil {
			panic(err)
		}
	}

	t := app.datastore.CreateTodo(todo)
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusCreated)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		panic(err)
	}
}
```

This function handles a `POST` request, so we `ioutil.ReadAll`  the body contents of the request. When then attempt to `Unmarshal` those read bytes into our `todo types.Todo` structure. If that fails, we have received either something other than JSON, or JSON but not in a format that defines a valid `Todo` structure, so we return `422` as our HTTP status and the `err` object thrown by `Unmarshal`. 

> **Note:** A more sophisticated app would do more validation on the JSON 

If the un-marshalling succeeded, we call `CreateTodo(todo)` on our datastore, which will add this new todo into our database. It’s important to note that our request handling code does not know how the data storing is implemented. The `todo` could be now stored in memory, in Redis on the some machine, in Amazon RDS, in S3, whatever. 

> **Note:** Our `CreateTodo(todo)` function should really return an `err` value if it fails, but this is just a basic demo app.

After datastore entry, we return `201 (Created)` back to the user to indicate that everything went as planned. 

#### The `datastore` Interface

I said just before that our interface hides the implementation details of our datastore so that it can vary independently of the rest of our application code. Let’s see how that works by checking out the `backend/datastores` directory, which has 2 implementations of the `Datastore` interface; In-memory, and Google Cloud Datastore. This is the interface that both have to implement:

```
// backend/datastores/core.go
type Datastore interface {
	ListTodos() types.Todos
	FindTodo(id string) types.Todo
	CreateTodo(t types.Todo) types.Todo
	DestroyTodo(id string) error
}
```

Pretty simple CRUD functions really. Here’s the full `backend/datastores/google_cloud_storage.go` file that uses a bucket to store a todo’s text as a string in a file that is named by the todo’s `id` (eg. 100.txt). 

```
package datastores

import (
	"io/ioutil"
	"path/filepath"
	"strings"

	log "github.com/sirupsen/logrus"
	"google.golang.org/api/iterator"

	"cloud.google.com/go/storage"
	"github.com/satori/go.uuid"
	"github.com/thundergolfer/golang-reactjs-skeleton-app/backend/types"
	"golang.org/x/net/context"
)

type GoogleCloudStorer struct {
	client     *storage.Client
	bucketName string
}

func NewGoogleCloudStorer(projectID string, bucketName string, ctx context.Context) *GoogleCloudStorer {
	storer := GoogleCloudStorer{
		bucketName: bucketName,
	}
	// Creates a client.
	client, err := storage.NewClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
		return nil
	}

	storer.client = client

	return &storer
}

func (s *GoogleCloudStorer) ListTodos() types.Todos {
	ctx := context.Background()

	todos := types.Todos{}

	bucket := s.client.Bucket(s.bucketName)
	it := bucket.Objects(ctx, nil)
	for {
		objAttrs, err := it.Next()
		if err != nil && err != iterator.Done {
			log.Warn(err)
			continue
		}
		if err == iterator.Done {
			break
		}
		if objReader, err := bucket.Object(objAttrs.Name).NewReader(ctx); err != nil {
			log.Warn(err) // Just skip this todo
			continue
		} else {
			slurp, err := ioutil.ReadAll(objReader)
			objReader.Close()
			if err != nil {
				log.Warn(err) // Just skip
				continue
			}

			idStr := strings.TrimSuffix(objAttrs.Name, filepath.Ext(objAttrs.Name))
			if err != nil {
				log.Warn("Found non-numeric .txt filename in Todos bucket")
				continue // Just skip it
			}

			todos = append(todos, types.Todo{
				Text: string(slurp),
				Id:   idStr,
			})
		}

	}
	return todos
}

// FindTodo retrieves a Todo obj from Google Cloud Storage if it exists.
// If it doesn't, the method will return an empty Todo
func (s *GoogleCloudStorer) FindTodo(id string) types.Todo {
	ctx := context.Background()
	// Creates a Bucket instance.
	bucket := s.client.Bucket(s.bucketName)

	objReader, err := bucket.Object(id + ".txt").NewReader(ctx)
	if err == nil {
		log.Warn(err)
		return types.Todo{}
	}

	slurp, err := ioutil.ReadAll(objReader)
	objReader.Close()
	if err != nil {
		log.Warn(err)
		return types.Todo{}
	}

	return types.Todo{
		Text: string(slurp),
	}

}

// CreateTodo stores a new Todo in Google Cloud Storage
func (s *GoogleCloudStorer) CreateTodo(t types.Todo) types.Todo {
	ctx := context.Background()

	t.Id = uuid.NewV4().String()
	wc := s.client.Bucket(s.bucketName).Object(t.Id + ".txt").NewWriter(ctx)

	wc.ContentType = "text/plain"
	wc.ACL = []storage.ACLRule{{storage.AllUsers, storage.RoleReader}}
	if _, err := wc.Write([]byte(t.Text)); err != nil {
		// TODO: handle error.
		// Note that Write may return nil in some error situations,
		// so always check the error from Close.
		log.Warn(err)
		return types.Todo{} // TODO: should return an err
	}
	if err := wc.Close(); err != nil {
		// TODO: handle error.
		log.Warn(err)
		return types.Todo{} // TODO: should return an err
	}

	return t
}

// DestroyTodo removes a Todo from Google Cloud Storage
func (s *GoogleCloudStorer) DestroyTodo(id string) error {
	ctx := context.Background()
	bucket := s.client.Bucket(s.bucketName)
	todoFile := id + ".txt"
	if err := bucket.Object(todoFile).Delete(ctx); err != nil {
		// TODO: Handle error.
		return err
	}
	return nil
}
```

Golang doesn’t have inheritance, but we can use *composition* to let our `GoogleCloudStorer` access all the methods of the `"cloud.google.com/go/storage"` package’s `Client` structure. It’s a nice feature of Go, and with it I seldom miss inheritance. 

```
type GoogleCloudStorer struct {
	client     *storage.Client
	bucketName string
}
```

I won’t show `backend/datastores/inmemory.go`, because it’s pretty simple and just uses a slice of `Todo`s to store our todos. 

#### Take a breath…

Done. That’s a backend with an API that can support our frontend, and be backed by any datastore you’d like (just implement the interface methods of `type Datastore interface`). 

### Setting up the ReactJS front-end

<!! PICTURE OF FRONTEND !!>

The key parts of our frontend implementation are the files in `frontend/src` and the `webpack.config.js` file. I’ll start with the Webpack file because they can honestly be confusing and it’ll be good to get it out of the way. 

#### The Webpack configuration file

```
var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'public/static/js');
var APP_DIR = path.resolve(__dirname, 'src');

var config = {
    entry: APP_DIR + '/index.js',
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js'
    },
    module : {
        loaders : [
            {
                test : /\.jsx?/,
                include : APP_DIR,
                loader : 'babel',
                query: { presets: ['react', 'es2015'] }
            }
        ]
    }
};

module.exports = config;
```

This isn’t too perverse. We specify `src/index.js` in the config files directory as the ‘main()’ file for starting the program. `output` specifies that we want the compiled result to end up in `public/static/js/bundle.js`, and in our `module` object we define that the `loaders` are to load `.js` or `.jsx` files from `src/` and allow for special ReactJS and ES2015 syntax. 

Config files can get a lot hairier than this, but fortunately our app is very simple, we don’t even compile our stylesheets, they’re just plain `.css`. 

### `frontend/src` 

Basically almost everything is in `frontend/src/index.js`, but there is `frontend/src/urls.js` file which I’ve used to separate out an object that contains the relevant API paths in the backend. It’s just a single path `/api/todos`, which we `GET`  and `DELETE` from, and `POST` or `PUT` to.

#### `index.js` 

> **Note:** Our frontend doesn’t [Redux](https://redux.js.org/introduction) because we’re keeping it simple. 

Right at the top we have imports and a simple ‘dumb’ component that receives data (how many open todos) and displays it. 

```
import React from 'react';
import { render } from 'react-dom';
import axios from 'axios';

import urls from './urls';

const Title = ({todoCount}) => {
  return (
    <div>
       <div>
          <h1><b>Golang+ReactJS Skeleton App</b></h1>
          <h2>To-Do ({todoCount})</h2>
       </div>
    </div>
  );
}
```

After that we have a `TodoForm` component which basically wraps a `<form />` HTML component and submits the text in our form’s textbox to the backend API via the `addTodo` function. 

```
const TodoForm = ({addTodo}) => {
  let input;
  return (
    <form onSubmit={(e) => {
        e.preventDefault();
        addTodo(input.value);
        input.value = '';
      }}>
      <input className="form-control col-md-12" ref={node => {
        input = node;
      }} />
      <br />
    </form>
  );
};
```

The `Todo` component just displays some text and when clicked calls the `remove` function passed in to mark the todo as ‘done’ (ie. delete it) in the backend API. The `TodoList` is a simple container that maps over a list of `Todo` components. Simple stuff. 

```
const Todo = ({todo, remove}) => {
  return (<a href="#" className="list-group-item" onClick={() => {remove(todo.id)}}>{todo.text}</a>);
}

const TodoList = ({todos, remove}) => {
  // Map through the todos
  const todoNode = todos.map((todo) => {
    return (<Todo todo={todo} key={todo.id} remove={remove}/>)
  });
  return (<div className="list-group" style={{marginTop:'30px'}}>{todoNode}</div>);
}
```

Finally we have our ‘smart’ component the `TodoApp`: 

```
class TodoApp extends React.Component{
  constructor(props){
    super(props);
    // Set initial state
    this.state = {
      data: []
    }
    this.apiUrl = urls.api.todos
  }
  componentDidMount(){
    axios.get(this.apiUrl)
      .then((res) => {
        this.setState({
          data: res.data
        });
      });
  }

  addTodo(val){
    const todo = {text: val}
    axios.post(this.apiUrl, todo)
       .then((res) => {
          this.state.data.push(res.data);
          this.setState({data: this.state.data});
       });
  }

  handleRemove(id){
    const remainder = this.state.data.filter((todo) => {
      if(todo.id !== id) return todo;
    });
    axios.delete(this.apiUrl+'/'+id)
      .then((res) => {
        this.setState({data: remainder});
      })
  }

  render(){
    return (
      <div>
        <Title todoCount={this.state.data.length}/>
        <TodoForm addTodo={this.addTodo.bind(this)}/>
        <TodoList
          todos={this.state.data}
          remove={this.handleRemove.bind(this)}
        />
      </div>
    );
  }
}
```

Here we find our function to add todos (called by our form on submit) and remove todos (called when you click a todo) and the `render()` function which wraps our app’s `Title` , `TodoForm` (the text box), and our `TodoList`, passing those component their data and functions.

Not noted yet is the React lifecycle method `componentDidMount` which will initialise our app’ state by calling `GET /api/todos` to get all current open todos. 

### Unanswered Questions You Might Have

**Q: How do the relative URLs resolve to be full URLs that point to the backend API?**

**Q: How do I run the frontend locally during development?**

**Q: Why is this setup good?**

**Q: How do I deploy this?**

`coming soon`

### Get the Code

Full code and `README.md` docs are at https://github.com/thundergolfer/golang-reactjs-skeleton-app. Please don’t hesitate to [create an issue](https://github.com/thundergolfer/golang-reactjs-skeleton-app/issues) if you have a problem or feedback. 
