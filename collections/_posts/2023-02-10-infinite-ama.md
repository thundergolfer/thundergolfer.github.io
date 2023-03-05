---
layout: page
title: Infinite AMA
date: 2023-02-10
summary: A ChatGPT that answers questions just like me.
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

<script src="https://unpkg.com/react@18.2.0/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.18.1/babel.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<!-- NOTE: This JS code has no linebreaks between definitions because linebreaks confuse my IDE's syntax highlighting. -->
<script type="text/babel">
    const Message = ({ message, index }) => {
        const icon = (message.isChatBot ? 
            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9aee86" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>
            : <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        );
        const extraMsgClassNames = message.isChatBot ? "bg-zinc-100 text-zinc-900" : "";
        const extraIconClassNames = message.isChatBot ? "" : "";
        let formattedMessage = message.text;
        if (message.isChatBot) {
            const markup = { __html: marked.parse(message.text) };
            formattedMessage = <div dangerouslySetInnerHTML={markup} />
        }
        return (
            <div className="flex flex-row p-2 mt-2 mb-2 mr-2 items-center">
                <span className={`rounded-md p-1 h-8 w-8 items-center ${extraIconClassNames}`}>{icon}</span>
                <span className={`rounded-lg ml-4 p-2 border border-zinc-300 w-full ${extraMsgClassNames}`}>{formattedMessage}</span>
            </div>
        );
    };
    const toChatHistory = (messages) => {
        /* The first is always from the human user */
        return messages.reduce(function(result, value, index, array) {
            if (index % 2 === 0 && (index + 1) < array.length) {
                result.push([array[index].text, array[index+1].text]);
            }
            return result;
        }, []);
    };
    const App = () => {
        const [error, setError] = React.useState("");
        const [loading, setLoading] = React.useState(false);
        const [textInput, setTextInput] = React.useState("");
        const [messages, setMessages] = React.useState([]);
        const prod = true;
        const apiEndpoint = prod ? "https://thundergolfer--infinite-ama.modal.run" : "https://thundergolfer--infinite-ama-dev.modal.run";
        React.useEffect(() => {
            if (messages.length === 0) return;
            const lastMessage = messages[messages.length-1];
            if (lastMessage.isChatBot) return;
            const userMessage = lastMessage;
            setLoading(true);
            async function updateStatus(userMessage) {
                const requestBody = {
                    text: userMessage.text,
                    history: toChatHistory(messages),
                };
                try {
                    const resp = await fetch(apiEndpoint, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(requestBody)
                    });
                    if (!resp.ok) {
                        setError(`HTTP error '${resp.status}'. Failed to get answer from API backend. Please try again.`);
                    } else {
                        const body = await resp.json();
                        if (body.error) {
                            setError(body.error);
                        } else {
                            addMessage(body.answer, true);
                        }
                    }
                } catch (error) {
                    const errMsg = error ? String(error) : "";
                    setError(error + " Failed to get answer from API backend. Please try again.");
                }
                setLoading(false);
            }
            updateStatus(userMessage);
        }, [messages]);
        const addMessage = (text, isChatBot) => {
            setMessages((prevMsgs) => [...prevMsgs, { text, isChatBot }]);
        };
        const onChange = (event) => {
            event.preventDefault();
            setTextInput(event.target.value);
        };
        const handleKeyDown = (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                addMessage(textInput, false);
                setTextInput("");
            }
        };
        const handleSubmit = (event) => {
            event.preventDefault();
            addMessage(textInput, false);
            setTextInput("");
        };
        return (
            <div>
                {messages.length === 0 ?
                    <section id="intro">
                        <div className="grid grid-cols-3 gap-4 text-md mt-8">
                            <div className="flex items-center justify-center ">
                            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>
                                <span className="m-4 font-medium">Examples</span>
                            </div>
                            <div className="flex items-center justify-center">
                            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" class="h-6 w-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"></path></svg>
                                <span className="m-4 font-medium">Capabilities</span>
                            </div>
                            <div className="flex items-center justify-center ">
                                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="11.4" y1="17" x2="12.60" y2="17"></line></svg>
                                <span className="m-4 font-medium">Limitations</span>
                            </div>
                        </div>
                        <div className="grid grid-rows-3 grid-flow-col gap-4 text-sm">
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200 cursor-pointer" onClick={() => setTextInput("What do you think of ChatGPT?")}>
                                <span className="m-4">"What do you think of ChatGPT?" →</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200 cursor-pointer" onClick={() => setTextInput("What's your job?")}>
                                <span className="m-4">"What's your job?" →</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md hover:bg-zinc-200 cursor-pointer" onClick={() => setTextInput("How do I build this AMA app in Modal?")}>
                                <span className="m-4">"How do I build this AMA app in Modal?" →</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">Remembers what user said earlier in the conversation.</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">Allows user to provide follow-up corrections.</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">Trained to decline inappropriate requests.</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">May faithfully reproduce my mistakes, or unfaithfully represent my true thoughts.</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">Constrained by OpenAI's lame but understandble corporate-friendly answer filtering.</span>
                            </div>
                            <div className="h-20 flex items-center  bg-zinc-100 rounded-md">
                                <span className="m-4">Trained on one man's knowledge and writing. I can't answer everything.</span>
                            </div>
                        </div>
                    </section>
                : undefined }
                <section id="#messages" className="mt-6">
                {messages.map((message, index) => (
                    <Message message={message} index={index} />
                ))}
                </section>
                {loading ?
                    <div class="flex flex-row p-2 mt-2 mb-2 mr-2 items-center" role="alert">
                        <span className="rounded-md p-1 h-8 w-8 items-center">
                            <svg className="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>
                        </span>
                        <div className="bg-blue-100 border text-blue-700 border-blue-400 w-full ml-4 p-2 rounded-md relative">
                            <strong class="font-bold">Jonathon's bot is typing...</strong>
                        </div>
                    </div>
                    : undefined
                }
                {error ?
                    <div class="flex flex-row p-2 mt-2 mb-2 mr-2 items-center" role="alert">
                        <span className="rounded-md p-1 h-8 w-8 items-center">
                            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#b91c1c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M16 16s-1.5-2-4-2-4 2-4 2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg>
                        </span>
                        <div className="bg-red-100 border text-red-700 border-red-400 w-full ml-4 p-2 rounded-md relative">
                            <strong class="font-bold">Error:</strong>
                            <span class="block sm:inline">{error}</span>
                            <button class="absolute top-0 bottom-0 right-0 m-2" onClick={() => setError("")}>
                                <svg class="fill-current h-6 w-6 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
                            </button>
                        </div>
                    </div>
                    : undefined
                }
                <div>
                    <form className="mt-12 mb-20 min-w-full rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)]">
                        <div className="min-w-full flex items-center py-2">
                            <input className="appearance-none bg-transparent border-none w-full text-gray-700 ml-2 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Ask me anything, anytime" aria-label="Full name" value={textInput} onChange={onChange} onKeyDown={handleKeyDown}></input>
                            <button className="flex-shrink-0 bg-stone-900 border-stone-900 hover:bg-blue-600 hover:border-blue-600 text-sm border-4 text-white py-1 px-2 rounded mr-2" type="button" onClick={handleSubmit}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
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
