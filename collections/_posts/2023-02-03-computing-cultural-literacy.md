---
layout: post
title: Computing Cultural Literacy
date: 2023-02-03
summary: What every programmer needs to know
categories: software culture
---

> Computing is pop culture. [...] Pop culture holds a disdain for history. Pop culture is all about identity and feeling like you're participating, It has nothing to do with cooperation, the past or the future—it's living in the present. I think the same is true of most people who write code for money. They have no idea where [their culture came from]. - Alan Kay

> We have ignored cultural literacy in thinking about education We ignore the air we breathe until it is thin or foul. Cultural literacy is the oxygen of social intercourse. - E. D. Hirsch Jr

To be culturally literate is to possess the basic information needed to thrive in the modern world. Computing cultural literacy is an overlapping but largely separate possession of basic information needed to thrive in today’s world of software and computing. Or is it needed at all? Did Jeff Bezos, sitting somewhere in Seattle in 1993 and watching internet traffic grow 230,000% need to know about UNIX, the Morris Worm, or Ada Lovelace in order to start [Amazon.com](http://Amazon.com) and become maybe the most successful software entrepreneur of all time? If one were to set down these _things to know_, would most programmers know them? Would you?

This idea of cultural literacy is taken directly from E. D. Hirsch Junior’s 1987 book _Cultural Literacy_. Hirsch Jr, a renowned education reformer, wanted the public to buy into great claims about knowledge-based literacy and the democratic, nation-building power of shared ideas. He lost the debate and his country’s institutions went other ways. In computing however, the debate has never been had. The one shot fired that is known to me comes from Alan Kay and is quoted above. He said that in a 2012 interview, and while he was clearly rankled, no one else cared to fight about it. Perhaps this field is too young, and does not yet have time for intro- and retro- spections.

Pop culture may have a disdain for the past, but coders won’t express a proud, rebuffing “we ain’t got no history”. Programmers tend to approach questions of providence and prior art as not so much unimportant but unnecessary. Come across people in the street tearing money out of a clear blue sky, and ask them where it came from. You’ll feel as a software historian may do, interrupting a party and asking if not for answers at least for someone to please take some notes.

But I have found that I’m on Kay’s side; there’s just so much back there, in the past. There’s [VARIOUS INTERESTING THINGS]

, and of course, people—a lot of people takingacid and soldering tools of enlightment, Turing award winners sitting in alone in college offices writing tomes all come to love and never read; Turing, who you’ll know made an eponymous machine and an AI test and was gay, but that’s not enough to know; couples spending nights at the Microsoft office, one at a keyboard one in a cot beside; people still _right_ _here_, in old file systems billions still use commenting things like "Error, skip block and hope for the best.”

Advancing cultural literacy is not revanchist. It does not want a rvtvrn to the old days when the term “software” sounded funny and it’s not a homework assignment. Let’s even concede that no one really _needs_ to know this stuff. But we should want to, because it’s just more fun, and with the knowledge we’ll do better work together. So—

[lest a whole new generation of programmers](http://www.catb.org/jargon/html/story-of-mel.html)

[grow up in ignorance of this glorious past,](http://www.catb.org/jargon/html/story-of-mel.html)

[I feel duty-bound to describe…](http://www.catb.org/jargon/html/story-of-mel.html)

## … 500 essential names, dates, and concepts

Following the the lead of the original book, here’s an attempt at a list of essential names, phrases, dates, and concepts in the computing and software community. E. D. Hirsch Junior’s list was an absurd 5,000 items; here I bother with only 500.

As with the original list, “knowing” something implies familiarity but not expertise.

The original list was also made collaboratively, and so is this one! The culture always moves, thinking left-to-right, at the right we have what’s slipping out of view and at the left is what is entering the core but remains fringe. You can indicate `left` when you find something to be ‘too left’, that is, exiting our culture into the past. Indicate `right` for the opposite, when something is ‘too right’, or too new. Undo with <kbd>⌘</kbd>+<kbd>z</kbd>, and submit suggestions with the button at the bottom.

### ¶ The list

<div class="flex-container">
    <div id="the-list-left" class="flex-left">
    </div>
    <div id="the-list-right" class="flex-right">
    </div>
</div>

<div class="submit-container">
    <button id="submit-suggestions" class="hidden" onclick="onSubmitSuggestions()"><span>📥</span> Submit suggestions</button>
</div>

<style>
.flex-container {
    display: flex;
    flex-direction: row;
}

.flex-container div {
    margin-right: 2.5em;
    width: 100%;
}

.flex-container div p {
    margin-bottom: 0.1em;
}

.flex-container div p span {
    margin-left: 0.5em;
}

button {
  color: #CCC;
  border: 1px solid #282828;
  font-family: Arial,Helvetica,sans-serif;
  background-color: #1f1f1f;
  -moz-box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px #141414 inset;
  -webkit-box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px #141414 inset;
  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px #141414 inset;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  border-radius: 3px;
  display: inline-block;
  margin: 0 0.1em;
  text-shadow: 0 1px 0 #999;
  line-height: 1.2;
  white-space: nowrap;
}


.button {
    display: none;
    padding: 0.1em 0.2em;
}

.flex-container p:hover .button {
    display: inline-block;
}

.flex-container .button:hover {
    /* Need to also show button when user hovers on the button, not the <p>. */
    display: inline-block; 
}

.button:hover, .button:focus, .button:active {
    color: white;
}

.faded {
    opacity: 0.5;
}

kbd{
  padding: 0.1em 0.4em;
  border: 1px solid #CCC;
  font-family: Arial,Helvetica,sans-serif;
  background-color: #F7F7F7;
  color: #333;
  -moz-box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px #ffffff inset;
  -webkit-box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px white inset;
  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2),0 0 0 2px white inset;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  border-radius: 3px;
  display: inline-block;
  margin: 0 0.1em;
  text-shadow: 0 1px 0 white;
  line-height: 1.2;
  white-space: nowrap;
}

.hidden {
    display: none !important;
}

.submit-container {
    display: flex; 
    justify-content: center;
    margin-top: 1.5em;
}

#submit-suggestions {
    color: white;
}

#submit-suggestions:hover {
    background: green;
}
</style>

<script>
    /* TODO: Support CTRL-Z undo of edits. */
    /* TODO: Support loading previous suggestion state from local storage. */
    /* TODO: Support calling serverless backend Modal endpoint. */
    
    items = ["+1", "1969", "1984 (advertisement)", "2001, January 1st", "2007, June 29", "10x programmer", "9 women can't produce a baby in 1 month", "abstract data type", "abstraction", "accidentally quadratic", "Amazon (company)", "AOL", "API", "Architecture", "Are we down?", "ARPANET", "array", "Art of Computer Programming, The", "Artificial intelligence", "As We May Think", "ASML", "Assembly", "Association for Computing Machinery", "Atlas Shrugged", "Audion", "Back-end", "Bad programmers worry about the code. Good programmers worry about data structures and their relationships.", "Ball of mud", "Bare metal", "Berkeley, Univesity of California", "Berkeley Software Distribution (BSD)", "Berners-Lee, Tim", "Bicycle for the mind", "Big-O", "BIOS", "Bit bashing, bit twiddling", "Bitcoin", "Blob", "Blog", "Body shop", "boot up", "Border Gateway Protocol (BGP)", "Browser", "Buffer overflow", "Bug", "Byte (magazine)", "C", "cache", "cache invalidation", "Cathedral and the Bazaar, The", "CD-ROM", "Chaos monkey", "chip", "Choose boring technology", "Client/Server", "Clippy", "Clock speed", "Cloud", "code monkey", "code review", "code smell", "command line", "comments", "Commodore", "Computer revolution, The", "considered harmful", "consistency", "Container", "cookies", "coredump", "Cray-1", "Crypto", "Cybernetics", "Cyberspace", "daemon", "Datacenter", "Data science", "DDOS (Distributed denial of service)", "DEC", "De Forest, Lee", "Dell Computers", "design doc", "DevOps", "dial-up", "disk", "Dean, Jeff", "Developers! Developers! Developers!", "Dijkstra, Edsger Wybe", "Distributed consensus", "Docker", "Doom", "Do the needful", "Don't repeat yourself (DRY)", "Eighty characters or less", "EMACS", "embarrassingly parallel", "End-to-end argument", "ENIAC", "exception", "Excel", "exploit", "event", "FAANG", "Fairchild Semiconductor", "Falsehoods Programmers Believe About X", "Fast inverse square root", "filesystem", "Finite automata", "firmware", "floating point", "Floppy disk", "fork", "fork bomb", "FORTRAN", "Free Software, Free Society", "front-end", "functional", "Garbage collection", "Gates, Bill", "Global Village", "Godel, Kurt", "God's own programming language", "GOTO", "Graybeard (or, Greybeard)", "grep", "hack", "Hackathon", "Hackernews", "Halting Problem, The", "Hamming, Richard", "hardcoded", "hash", "Hello world!", "Hey! Get back to work!; Compiling!", "Hierarchy of the grammars", "High-Tech Employee Antitrust Litigation", "Homebrew", "Hopper, Grace", "hotfix", "HyperCard", "Hypertext", "I just want to serve 5TB", "IBM", "IEEE", "I'm feeling lucky", "Incompleteness Theorem", "infinite loop", "Information retreival", "Information superhighway", "Innovator's dilemma", "Instance", "instruction", "Intel", "Interactive development environment (IDE)", "IRC", "It's always DNS", "it works on my machine", "Java", "Javascript", "Jobs, Steve", "Kay, Alan", "Kernighan, Brian W.", "kernel", "Knuth cheque", "Kubernetes", "Lamport, Leslie", "latency", "learn to code", "Leetcode", "legacy codebase", "library", "LINGsCARS.com", "Linux", "Liskov substitution principle", "Literate programming", "Little's Law", "log", "looks good to me (LGTM)", "Lovelace, Ada", "magic numbers", "map-reduce", "Markup", "Master/slave", "mechanical keyboard", "Meltdown", "memory hierarchy", "memory leak", "Menlo Park, Californa", "Metaverse", "Microservice", "Minsky, Marvin", "modem", "monad", "monolith", "Moore's Law", "Mother of all demos", "mouse", "Mountain View, Californa", "multitasking", "mutex", "MVP", "Netscape", "network", "nits", "No modes (saying)", "No silver bullet", "Nobody ever got fired for buying IBM", "non-technical", "Null", "Object-oriented", "off-by-one", "'Only two hard problems in ...'", "on-prem", "onsite", "Operating system", "Our incredible journey", "outage", "overclock", "over-engineered", "P = NP", "PaaS", "Pagerank", "parser", "Parse, don't validate", "PDP-7, PDP-11", "Perlis, Alan J", "persistent", "personal computer", "pets and cattle", "Phone screen", "pipe it", "Pointer", "portable", "Pragmatic Programmer, The", "preformatted", "premature optimization is the root of all evil", "problem exists between keyboard and computer (PEBKAC)", "punch card", "Python", "queue", "Quicksort", "RAID", "Rails", "React", "Real Programmer", "recursion", "Redis", "Reduced Instruction Set Architecture (RISC)", "Reflections on Trusting Trust (title)", "relational", "request for comment (RFC)", "Rest and vest", "REST (Respresentional state transfer)", "Ritchie, Dennis", "RSS feed", "RSUs", "SaaS", "Sand Hill Road", "SAT problem", "scalability", "Scripting", "Script kiddie", "Scrum", "search", "Security by Obscurity", "Self-taught", "Semantic Web", "Semaphore", "Sequence diagram", "Series A, B, C, ...", "Serverless", "Shannon, Claude", "Shell", "Shenzhen, China", "Ship it!", "Side project", "Silicon valley", "Simon, Herbert", "SOLID principles", "spagetti code", "Spinning disk", "Sprint", "SQL", "Sqlite", "Stack overflow", "StackOverflow.com", "Stallman, Richard", "Story of Mel", "Story point", "Stream", "Stuxnet", "subroutine", "Sun Microsystems", "symbolic", "Sysadmin", "syscall", "System 360", "Systems programming", "Swartz, Aaron", "tabs or spaces", "Taiwan Semiconductor Manufacturing Company", "TCP/IP", "terminal", "test-driven development (TDD)", "The key, the whole key, and nothing but the key, so help me Codd.", "Thompson, Ken", "Three nines", "Time-sharing", "Torvalds, Linus", "Traitorous eight", "Transaction", "Transhumanism", "Tree (structure)", "Tu- Tu- Tu- Tu- uring, Alan", "Turn on, tune in, drop out","UML", "Unix", "Unreasonable effectiveness of ..., The", "utils", "Venture capital", "Vim", "virtual", "Virtual machine", "Virtual memory", "Web 2.0", "web3", "webscale", "webshit", "Windows NT", "Wired (magazine)", "Wirth, Niklaus", "working set", "worse is better", "Wozniak, Steve", "x86", "Xeroz PARC", "y2k", "Yahoo.com", "Yak shave", "YCombinator", "Yet Another ...", "You ain't gonna need it (YAGNI)", "Zero day", "Zero to One", "Zuckerberg, Mark"];

    /**
    * @param {String} HTML representing a single element
    * @return {Element}
    */
    const htmlToElem = (html) => {
        var template = document.createElement("template");
        /* Never return a text node of whitespace as the result */
        html = html.trim();
        template.innerHTML = html;
        return template.content.firstChild;
    };

    let listLeft = document.getElementById("the-list-left");
    let listRight = document.getElementById("the-list-right");
    let middleIdx = Math.floor(items.length / 2);
    for (let i = 0; i < items.length; i++) {
        let child = htmlToElem(`
            <p>
                ${items[i]}
                <span>
                    <button class="button" onclick="onLeft(this)">←</button>
                    <button class="button" onclick="onTrash(this)">🗑️</button>
                    <button class="button" onclick="onRight(this)">→</button>
                </span>
            </p>
        `);

        if (i <= middleIdx) {
            listLeft.appendChild(child);
        } else {
            listRight.appendChild(child);
        }
    }

    const $submitSuggestionsBtn = document.getElementById("submit-suggestions");
    
    const ITEM_STATE = {
        LEFT: "LEFT",
        TRASH: "TRASH",
        RIGHT: "RIGHT"
    };
    let itemToState = new Map();

    function setSuggestionsBtnState() {
        if (itemToState.size > 0) {
            $submitSuggestionsBtn.classList.remove("hidden");
        } else {
            $submitSuggestionsBtn.classList.add("hidden");
        }
    };

    function onLeft(elem) {
        console.log("clicked LEFT");
        console.log(elem.parentNode.parentNode);
        /* WARN: coupled to HTML structure. */
        let itemText = elem.parentNode.parentNode.firstChild.textContent.trim();
        itemToState.set(itemText, ITEM_STATE.LEFT);
        elem.parentNode.parentNode.classList.add("faded");
        console.log(itemToState);
        setSuggestionsBtnState();
    };

    function onRight(elem) {
        console.log("clicked RIGHT");
        console.log(elem.parentNode.parentNode);
        /* WARN: coupled to HTML structure. */
        let itemText = elem.parentNode.parentNode.firstChild.textContent.trim();
        itemToState.set(itemText, ITEM_STATE.RIGHT);
        elem.parentNode.parentNode.classList.add("faded");
        console.log(itemToState);
        setSuggestionsBtnState();
    };

    function onTrash(elem) {
        console.log("clicked TRASH");
        console.log(elem.parentNode.parentNode);
        /* WARN: coupled to HTML structure. */
        let itemText = elem.parentNode.parentNode.firstChild.textContent.trim();
        itemToState.set(itemText, ITEM_STATE.TRASH);
        elem.parentNode.parentNode.classList.add("faded");
        console.log(itemToState);
        setSuggestionsBtnState();
    };

    apiRoot = "https://thundergolfer--comp-lit-stats-web.modal.run";
    addSuggestionsEndpoint = `${apiRoot}/add`;
    function onSubmitSuggestions() {
        console.log(`Submitting ${itemToState.size} suggestions`);
        let requestBody = {
            left: [],
            right: [],
            trash: [],
        };
        for (let [key, value] of itemToState) {
            switch (value) {
                case ITEM_STATE.LEFT:
                    requestBody.left.push(key);
                    break;
                case ITEM_STATE.RIGHT:
                    requestBody.right.push(key);
                    break;
                case ITEM_STATE.TRASH:
                    requestBody.trash.push(key);
                    break;
                default:
                    console.log(`Unknown state for key '${key}' ${value}`);
            }
        }
        $submitSuggestionsBtn.innerText = `⏳ Submitting ${itemToState.size} suggestions...`;
        try {
            fetch(addSuggestionsEndpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestBody),
            }).then((response) => {
                if (!response.ok) {
                    $submitSuggestionsBtn.innerText = `❌ Failed to submit ${itemToState.size} suggestions. Please try again!`;
                } else {
                    $submitSuggestionsBtn.innerText = `📨 Submitted ${itemToState.size} suggestions. Thanks!`;
                    /* TODO: Disable button. */
                }
            });
        } catch (error) {
            $submitSuggestionsBtn.innerText = `❌ Failed to submit ${itemToState.size} suggestions. Please try again!`;
        }

    }

    document.addEventListener("keydown", function(e) {
        if (e.keyCode >= 65 && e.keyCode <= 90) {
            console.log("UNDO!");
        }
    });
</script>
