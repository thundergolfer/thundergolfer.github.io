---
layout: page
title: Infinite AMA
date: 2023-02-10
summary: A ChatGPT that answers questions just like me
categories: chatbot llm
permalink: infinite-ama
---

A thing built by me to amuse you.

<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
    theme: {
    extend: {
        colors: {
        clifford: '#da373d',
        }
    }
    }
}
</script>

<section id="app">
    <!-- React DOM renders here -->
    <div id="wrap"></div>
</section>

<script src="https://unpkg.com/react@15/dist/react.min.js"></script>
<script src="https://unpkg.com/react-dom@15/dist/react-dom.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.24/browser.min.js"></script>
<script type="text/babel">
    class App extends React.Component {
        constructor(props) {
            super(props);
        };
        render() {
            const message = "Jono here!!";
            return (
                <div>
                    <div className="grid grid-cols-3 gap-4 text-md mt-4">
                        <div className="flex items-center justify-center ">
                        <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>
                            <span className="m-4 font-medium">Examples</span>
                        </div>
                        <div className="flex items-center justify-center">
                        <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" class="h-6 w-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"></path></svg>
                            <span className="m-4 font-medium">Capabilities</span>
                        </div>
                        <div className="flex items-center justify-center ">
                            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                            <span className="m-4 font-medium">Limitations</span>
                        </div>
                    </div>
                    <div className="grid grid-rows-3 grid-flow-col gap-4 text-sm">
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200">
                            <span className="m-4">"Explain quantum computing in simple terms" →</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200">
                            <span className="m-4">"Got any creative ideas for a 10 year olds birthday?" →</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200">
                            <span className="m-4">"How do I build this AMA app in Modal?" →</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">Remembers what user said earlier in the conversation</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">Allows user to provide follow-up corrections</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">Trained to decline inappropriate requests</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">May occasionally generate incorrect information</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">May occasionally produce harmful instructions or biased content</span>
                        </div>
                        <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                            <span className="m-4">Limited knowledge of world and events after 2021</span>
                        </div>
                    </div>
                    <div>
                        <form className="mt-12 min-w-full rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)]">
                            <div className="min-w-full flex items-center py-2">
                                <input className="appearance-none bg-transparent border-none w-full text-gray-700 ml-2 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Jane Doe" aria-label="Full name"></input>
                                <button className="flex-shrink-0 bg-stone-900 border-stone-900 hover:bg-blue-600 hover:border-blue-600 text-sm border-4 text-white py-1 px-2 rounded mr-2" type="button">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            );
        }
    };
    ReactDOM.render(
        <App />,
        document.getElementById('wrap')
    );
</script>

<style>
.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

</style>

{% include
  subscribe.html %}
