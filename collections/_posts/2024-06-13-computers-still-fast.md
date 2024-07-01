---
layout: post
title: Computers are fast
date: 2024-06-13
summary: Do you know how much your computer can do in one second?
categories: performance programming modal
---

Let's find out how well you know computers!

All of these programs have a variable **`N`** in them. Your mission: guess how big **`N`** must get before the program takes 1 second to run.

You don't need to guess exactly. Just try to guess the right order of magnitude!
The options are all between 1 and one billion.

### But first, some introductory points

- If the answer is 38,400, both 10,000 and 100,000 are considered correct answers.
  The goal is to not be wrong by more than 10x, one order of magnitude 🤓.
- We know computers have different disk & network & CPU speeds! We're trying to understand the difference between code that can run ten times a second (10 Hz) and 100,000 times a second (100 KHz). A newer computer won't make any of the benchmark code run 1000x faster.
  - That said, the results are from running on an 2023 Mac M2 Max.
- The 🦀 code was compiled with `--release`, of course.

Good luck! The first time I tried [**the original quiz**](https://computers-are-fast.github.io/) (2014) I did decently but got a handful wrong. Each surprise is an invitation to question assumptions, and learn something new!

<!-- Quiz -->
<div class="quiz-container">
    <div id="language-selector">
        <div id="btn-rust" class="toggle-button" onclick="handleButtonClick('rust')"><strong>Rust</strong></div>
        <div id="btn-python" class="toggle-button" onclick="handleButtonClick('python')"><strong>Python</strong></div>
    </div>
    <div class="score-container" id="score-container">
        <strong>Score:</strong> <span id="score">0</span>/<span id="answered">0</span><br>
        <strong>Unanswered:</strong> <span id="unanswered">0</span>
    </div>
    <div id="quiz"></div>
</div>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/night-owl.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/rust.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tsparticles/confetti@3.0.3/tsparticles.confetti.bundle.min.js"></script>
<script>
    const pyQuestions = [{"name": "bench_dict_mutation", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10000000, "answer_duration_ms": 998.5780334100127, "estimated_n": 29654986, "bench_source": "d = {}\nmax_entries = 1000\nfor i in range(n):\n    d[i % max_entries] = i", "bench_doc": "Number to guess: How many entries can we add to a dictionary in a second?", "hints": []}, {"name": "bench_loop", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 100000000, "answer_duration_ms": 999.0589584223926, "estimated_n": 111447253, "bench_source": "for _ in range(n):\n    pass", "bench_doc": "Number to guess: How many iterations of an empty loop can we go through in a second?\n", "hints": ["A CPU can execute around a few billion instructions per second."]}, {"name": "bench_parse_http_request", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10000, "answer_duration_ms": 1016.977958381176, "estimated_n": 81029, "bench_source": "class HTTPRequest(BaseHTTPRequestHandler):\n    def __init__(self, request_text):\n        self.rfile = BytesIO(request_text)\n        self.raw_requestline = self.rfile.readline()\n        self.error_code = self.error_message = None\n        self.parse_request()\n\n    def send_error(self, code, message):\n        self.error_code = code\n        self.error_message = message\n\nrequest_text = b\"\"\"GET / HTTP/1.1\nHost: localhost:8001\nConnection: keep-alive\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\nAccept-Encoding: gzip, deflate, sdch\nAccept-Language: en-GB,en-US;q=0.8,en;q=0.6\n\"\"\"\nfor _ in range(n):\n    _ = HTTPRequest(request_text)", "bench_doc": "Number to guess: How many HTTP GET requests can we parse in a second?", "hints": []}, {"name": "bench_run_python", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10, "answer_duration_ms": 939.4294084049761, "estimated_n": 82, "bench_source": "for _ in range(n):\n    subprocess.run(\"python3 -c ''\", shell=True, check=True)", "bench_doc": "Number to guess: How many times can we start the Python interpreter in a second?", "hints": ["This is much less than 100 million :)"]}, {"name": "bench_write_to_disk", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 1000000000, "answer_duration_ms": 1080.6438165716827, "estimated_n": 3862626348, "bench_source": "def cleanup(f, name):\n    f.flush()\n    os.fsync(f.fileno())\n    f.close()\n    try:\n        os.remove(name)\n    except OSError:\n        pass\n\nchunk_size = 1_000_000  # 1 megabyte\ndata_chunk = b\"a\" * chunk_size\nname = \"/tmp/bench-write-to-disk\"\nbytes_written = 0\nwith open(name, 'wb') as f:\n    while bytes_written < n:\n        written = f.write(data_chunk)\n        bytes_written += chunk_size\n        assert written == chunk_size, \"incomplete disk write\"\n    cleanup(f, name)", "bench_doc": "Number to guess: How many bytes can we write to an output file in a second?", "hints": ["we make sure everything is sync'd to disk before exiting"]}, {"name": "bench_write_to_memory", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 1000000000, "answer_duration_ms": 1060.419808421284, "estimated_n": 10281010020, "bench_source": "chunk_size = 1_000_000  # 1 megabyte\ndata_chunk = \"a\" * chunk_size\noutput = StringIO()\nbytes_written = 0\nwhile bytes_written < n:\n    _ = output.write(data_chunk)\n    bytes_written += chunk_size\noutput.getvalue()", "bench_doc": "Number to guess: How many bytes can we write to a string in memory in a second?", "hints": []}];
    const rustQuestions = [{"name":"bench_loop","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":290.0,"estimated_n":3448275862,"bench_source":"{ for _ in 0 .. n { black_box(()); } }","bench_doc":" Number to guess: How many iterations of an empty loop can we go through in a second?","hints":["A CPU can execute around a few billion instructions per second."],"language":"rust"},{"name":"bench_dict_mutation","platform":"Darwin-13.4-arm64","lang_version":"","answer":100000000,"answer_duration_ms":822.0,"estimated_n":121654501,"bench_source":"{\n    let mut m = HashMap :: new(); let max_entries = 1000; for i in 0 .. n\n    { m.insert(i % max_entries, i); }\n}","bench_doc":" Number to guess: How many entries can we add to a std::HashMap in a second?","hints":null,"language":"rust"},{"name":"bench_download_webpage","platform":"Darwin-13.4-arm64","lang_version":"","answer":1,"answer_duration_ms":136.0,"estimated_n":7,"bench_source":"{\n    for _ in 0 .. n\n    {\n        let mut stream = TcpStream :: connect(\"google.com:80\").unwrap(); let\n        request =\n        \"GET / HTTP/1.1\\r\\nHost: google.com\\r\\nConnection: close\\r\\n\\r\\n\";\n        stream.write_all(request.as_bytes()).unwrap(); let mut response =\n        String :: new(); stream.read_to_string(& mut response).unwrap();\n    }\n}","bench_doc":" Number to guess: How many times can we download google.com in a second?","hints":null,"language":"rust"},{"name":"bench_run_python","platform":"Darwin-13.4-arm64","lang_version":"","answer":10,"answer_duration_ms":107.0,"estimated_n":93,"bench_source":"{\n    for _ in 0 .. n\n    {\n        let mut child = std :: process :: Command ::\n        new(\"python3\").args([\"-c\",\n        \"''\"]).spawn().expect(\"failed to execute child\"); let ecode =\n        child.wait().expect(\"failed to wait on child\"); assert!\n        (ecode.success());\n    }\n}","bench_doc":" Number to guess: How many times can we start the Python interpreter in a second?","hints":["This is much less than 100 million :)"],"language":"rust"},{"name":"bench_write_to_disk","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":447.0,"estimated_n":2237136465,"bench_source":"{\n    const CHUNK_SIZE : usize = 1_000_000; let data_chunk : [u8; CHUNK_SIZE] =\n    [b'a'; CHUNK_SIZE]; let mut f = std :: fs :: File ::\n    create(\"/tmp/bench-write-to-disk\").unwrap(); let mut bytes_written = 0;\n    while bytes_written < n\n    {\n        let written = f.write(& data_chunk).unwrap(); bytes_written +=\n        CHUNK_SIZE as u64; assert_eq!\n        (written, CHUNK_SIZE, \"incomplete disk write\");\n    } f.sync_all().unwrap();\n}","bench_doc":" Number to guess: How many bytes can we write to an output file in a second?","hints":null,"language":"rust"},{"name":"bench_write_to_memory","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":179.0,"estimated_n":1291624882,"bench_source":"{\n    const CHUNK_SIZE : usize = 1_000_000; let data_chunk : [u8; CHUNK_SIZE] =\n    [b'a'; CHUNK_SIZE]; let mut buffer : Vec < u8 > = vec! []; let mut\n    bytes_written = 0; while bytes_written < n\n    { buffer.extend(& data_chunk); bytes_written += CHUNK_SIZE as u64; }\n    assert! (buffer.len() >= n as usize);\n}","bench_doc":" Number to guess: How many bytes can we write to a string in memory in a second?","hints":null,"language":"rust"}];
    const options = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000].map((n) => n.toLocaleString());
    let score = 0;
    let answered = 0;
    let unanswered = 0;
    function handleButtonClick(language) {
        const buttons = document.querySelectorAll('.toggle-button');
        buttons.forEach(button => button.classList.remove('selected'));
        const selectedButton = document.getElementById(`btn-${language}`);
        selectedButton.classList.add('selected');
        createQuiz(language);
    }
    function createQuiz(language) {
        const questions = language == 'python' ? pyQuestions : rustQuestions;
        /* Reset counters, score-box. */
        score = 0;
        answered = 0;
        unanswered = questions.length;
        document.getElementById('score').textContent = score;
        document.getElementById('answered').textContent = answered;
        document.getElementById('unanswered').textContent = unanswered;
        updateScoreColor();
        const quizContainer = document.getElementById('quiz');
        quizContainer.innerHTML = ''; /* reset */
        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            const questionHeading = document.createElement('h3');
            questionHeading.textContent = question.name;
            questionDiv.appendChild(questionHeading);
            const questionText = document.createElement('p');
            questionText.textContent = question.bench_doc;
            questionDiv.appendChild(questionText);
            if (question.hints && question.hints.length > 0) {
                const questionHints = document.createElement('div');
                questionHints.classList.add('hover-reveal');
                let hoverText = fromHTML('<span class="hover-text"><em>Hints</em></span>');
                const questionHintsUL = document.createElement('ul');
                questionHintsUL.classList.add('hover-content');
                question.hints.forEach(hint => {
                    const li = document.createElement('li');
                    li.textContent = hint;
                    questionHintsUL.appendChild(li);
                });
                questionHints.appendChild(hoverText);
                questionHints.appendChild(questionHintsUL);
                questionDiv.appendChild(questionHints);
            }
            const questionPre = document.createElement('pre');
            const questionCode = document.createElement('code');
            questionPre.appendChild(questionCode);
            questionCode.textContent = question.bench_source;
            questionCode.classList.add(`language-${language}`);
            questionDiv.appendChild(questionPre);
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options';
            options.forEach(option => {
                const button = document.createElement('button');
                button.textContent = option;
                button.onclick = () => checkAnswer(language, button, question.answer, question.estimated_n, questionDiv);
                optionsDiv.appendChild(button);
            });
            questionDiv.appendChild(optionsDiv);
            quizContainer.appendChild(questionDiv);
        });
        document.getElementById('unanswered').textContent = unanswered;
        hljs.highlightAll();
    }
    function checkAnswer(language, button, correctAnswer, exactAnswer, questionDiv) {
        const allButtons = button.parentElement.children;
        for (let btn of allButtons) {
            const btnAnswer = parseInt(btn.textContent.replace(/,/g, ''));
            btn.disabled = true;
            if (btnAnswer === correctAnswer) {
                btn.classList.add('correct');
            } else if ((correctAnswer < exactAnswer) && (btnAnswer / 10) == correctAnswer) {
                btn.classList.add('correct');
            } else if ((correctAnswer > exactAnswer) && (btnAnswer * 10) == correctAnswer) {
                btn.classList.add('correct');
            }
        }
        const givenAnswer = parseInt(button.textContent.replace(/,/g, ''));
        console.log(`correct: ${correctAnswer} exact: ${exactAnswer} given: ${givenAnswer}; 1: ${(givenAnswer / 10) == correctAnswer} 2: ${(givenAnswer * 10) == correctAnswer}`);
        /* correct: 10 exact: 82 given: 100 */
        if (givenAnswer === correctAnswer) {
            score++;
            document.getElementById('score').textContent = score;
        } else if ((correctAnswer < exactAnswer) && (givenAnswer / 10) == correctAnswer) {
            score++;
            document.getElementById('score').textContent = score;
        } else if ((correctAnswer > exactAnswer) && (givenAnswer * 10) == correctAnswer) {
            score++;
            document.getElementById('score').textContent = score;
        } else {
            button.classList.add('wrong');
        }
        unanswered--;
        answered++;
        document.getElementById('score').textContent = score;
        document.getElementById('answered').textContent = answered;
        document.getElementById('unanswered').textContent = unanswered;
        /* Show exact answer now that user has submitted their guess */ 
        const exactAnswerText = document.createElement('p');
        exactAnswerText.className = 'exact-answer';
        exactAnswerText.innerHTML = `<strong>Answer:</strong> ${exactAnswer.toLocaleString()}`;
        questionDiv.appendChild(exactAnswerText);
        updateScoreColor();
        /* Celebrate perfect score! */
        if (unanswered === 0 && score === answered) {
            const langColors = language == "python" ? ["FFDE57", "4584B6"] : ["B7410E", "0EB7A1", "0A8071", "B77F0E"];
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 },
                colors: langColors,
            });
        }
    }
    /* 
    Give user feedback on their performance by coloring the score box according to % of
    correct guesses.
    */
    function updateScoreColor() {
        const scoreElement = document.getElementById('score-container');
        const percentage = score / answered;
        const green = Math.floor(percentage * 200);
        const red = Math.floor((1 - percentage) * 200);
        scoreElement.style.color = `rgb(${red}, ${green}, 50)`;
    }
    /**
     * @param {String} HTML representing a single element.
     * @param {Boolean} flag representing whether or not to trim input whitespace, defaults to true.
     * @return {Element | HTMLCollection | null}
     */
    function fromHTML(html, trim = true) {
        html = trim ? html.trim() : html;
        if (!html) return null;
        /* Then set up a new template element. */
        const template = document.createElement('template');
        template.innerHTML = html;
        const result = template.content.children;
        /* Then return either an HTMLElement or HTMLCollection,
        based on whether the input HTML had one or more roots. */
        if (result.length === 1) return result[0];
        return result;
    }
    createQuiz('python');
</script>
<!-- End Quiz -->

Disappointed in your score? I'd recommend checking out [teachyourselfcs.com](https://teachyourselfcs.com/) and [sirupsen/napkin-math](https://github.com/sirupsen/napkin-math).

By studying napkin math, operating systems, and computer architecture I got a lot better at estimating
program performance.

<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Panel info">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <path d="M12 20a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm0-8.5a1 1 0 0 0-1 1V15a1 1 0 0 0 2 0v-2.5a1 1 0 0 0-1-1zm0-1.125a1.375 1.375 0 1 0 0-2.75 1.375 1.375 0 0 0 0 2.75z" fill="currentColor" fill-rule="evenodd"></path>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            The code for these benchmarks is at <a href="https://github.com/thundergolfer/uni/tree/main/performance/computers-are-fast">github.com/thundergolfer/uni/tree/main/performance/computers-are-fast</a>
        </p>
    </div>
</div>

<style>
    .quiz-container {
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .question {
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .options button {
        margin: 5px;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        border-style: solid;
        border-width: 1px;
        border-radius: 0.25em;
        border-color: hsla(0, 0%, 0%, .2);
    }
    .correct {
        background-color: green;
        color: white;
    }
    .wrong {
        background-color: red;
        color: white;
    }
    pre {
        padding: 0;
    }
    .score-container {
        position: fixed;
        right: 5em;
        top: 50%;
        transform: translateY(-50%);
        padding: 20px;
        background: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-size: 18px;
    }
    .exact-answer {
        margin-top: 10px;
        color: #333;
    }
    .hover-reveal {
        position: relative;
        display: inline-block;
        cursor: pointer;
        margin-bottom: 10px;
        background-color: #B6D0E2;
        border-radius: 3px;
    }

    .hover-reveal .hover-content {
        display: none;
        z-index: 1;
        color: #f9f9f9;
        padding: 5px;
        margin-left: 15px;
    }

    .hover-reveal:hover .hover-content {
        display: block;
    }

    .hover-reveal .hover-text {
        display: inline-block;
        color: white;
        padding: 5px;
    }

    .hover-reveal:hover .hover-text {
        display: none;
    }

    .hover-reveal ul {
        margin-bottom: 0;
        padding-right: 0.5em;
    }
    #language-selector {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5em;
    }
    .toggle-button {
        display: inline-block;
        padding: 10px 20px;
        border: 2px solid #ccc;
        border-radius: 5px;
        cursor: pointer;
        user-select: none;
        width: 43%;
    }
    .selected {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
    }
    @media screen and (max-width: 1268px) {
        #score-container {
            display: none;
        }
    }
</style>

<style>
.callout-panel {
    border-radius: 3px;
    margin: 1.2rem 0px 1.2rem 0px;
    padding: 20px;
    min-width: 48px;
    display: flex;
    /*-webkit-box-align: baseline;*/
    /*align-items: baseline;*/
    word-break: break-word;
    border: none;
}

.callout-panel p {
    margin-bottom: 0;
    line-height: 24px;
}

.callout-panel-icon {
    display: block;
    flex-shrink: 0;
    height: 24px;
    width: 24px;
    box-sizing: content-box;
    padding-right: 8px;
    color: rgb(0, 82, 204);
}


.callout-panel-info {
    background-color: rgb(250, 250, 255);
}

.callout-panel-info-icon {
    color: blue;
}

.callout-panel-warning {
    background-color: rgb(255, 250, 200);
}

.callout-panel-warning-icon {
    color: orange;
}

</style>
