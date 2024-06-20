---
layout: post
title: Computers are fast
date: 2024-06-13
summary: Do you know how much your computer can do in one second?
categories: performance programming modal
---

Let's find out how well you know computers! 

All of these programs have a variable `N` in them. Your mission: guess how big `N` needs to get before the program takes 1 second to run.

You don't need to guess exactly. Just try to guess the right order of magnitude!
The options are all between 1 and one billion. 

### But first, some introductory points

- If the answer is 38,400, both 10,000 and 100,000 are considered correct answers. 
The goal is to not be wrong by more than 10x, one order of magnitude 🤓.
- We know computers have different disk & network & CPU speeds! We're trying to get understand difference between code that can run ten times a second (10 Hz) and 100,000 times a second (100 KHz). A newer computer won't make any of the benchmark code run 1000x faster.
- That said, the results are from running on an 2023 Mac M2 Max and Modal's beefy Oracle Cloud workers. 
- The 🦀 code was compiled with `--release`, of course!.

Good luck! The first time I tried [the original quiz](https://computers-are-fast.github.io/) I did decently but got a handful wrong. Each surprise is an invitation to question assumptions, learn something new.


<!-- Quiz -->
<div class="quiz-container">
    <div class="score-container" id="score-container">
        <strong>Score:</strong> <span id="score">0</span>/<span id="answered">0</span><br>
        <strong>Unanswered:</strong> <span id="unanswered">0</span>
    </div>
    <div id="quiz"></div>
</div>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<script>
    const questions = [{"name": "bench_dict_mutation", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10000000, "answer_duration_ms": 1009.2619582079352, "estimated_n": 28180832, "bench_source": "d = {}\nmax_entries = 1000\nfor i in range(n):\n    d[i % max_entries] = i", "bench_doc": "Number to guess: How many entries can we add to a dictionary in a second?"}, {"name": "bench_loop", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 100000000, "answer_duration_ms": 991.8014083988965, "estimated_n": 110140017, "bench_source": "for _ in range(n):\n    pass", "bench_doc": "Number to guess: How many iterations of an empty loop can we go through in a second?\n\nHints:\n- todo"}, {"name": "bench_parse_http_request", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10000, "answer_duration_ms": 987.7103500068188, "estimated_n": 75477, "bench_source": "class HTTPRequest(BaseHTTPRequestHandler):\n    def __init__(self, request_text):\n        self.rfile = BytesIO(request_text)\n        self.raw_requestline = self.rfile.readline()\n        self.error_code = self.error_message = None\n        self.parse_request()\n\n    def send_error(self, code, message):\n        self.error_code = code\n        self.error_message = message\n\nrequest_text = b\"\"\"GET / HTTP/1.1\nHost: localhost:8001\nConnection: keep-alive\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\nAccept-Encoding: gzip, deflate, sdch\nAccept-Language: en-GB,en-US;q=0.8,en;q=0.6\n\"\"\"\nfor _ in range(n):\n    _ = HTTPRequest(request_text)", "bench_doc": "Number to guess: How many HTTP GET requests can we parse in a second?"}, {"name": "bench_run_python", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 10, "answer_duration_ms": 925.1868666149676, "estimated_n": 73, "bench_source": "for _ in range(n):\n    subprocess.run(\"python3 -c ''\", shell=True, check=True)", "bench_doc": "Number to guess: How many times can we start the Python interpreter in a second?\n\nHints:\n- This is much less than 100 million :)"}, {"name": "bench_write_to_disk", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 1000000000, "answer_duration_ms": 1001.9655417650939, "estimated_n": 3194939218, "bench_source": "def cleanup(f, name):\n    f.flush()\n    os.fsync(f.fileno())\n    f.close()\n    try:\n        os.remove(name)\n    except OSError:\n        pass\n\nchunk_size = 1_000_000  # 1 megabyte\ndata_chunk = b\"a\" * chunk_size\nname = \"/tmp/bench-write-to-disk\"\nbytes_written = 0\nwith open(name, 'wb') as f:\n    while bytes_written < n:\n        written = f.write(data_chunk)\n        bytes_written += chunk_size\n        assert written == chunk_size, \"incomplete disk write\"\n    cleanup(f, name)", "bench_doc": "Number to guess: How many bytes can we write to an output file in a second?\n\nHints: \n- we make sure everything is sync'd to disk before exiting :)"}, {"name": "bench_write_to_memory", "platform": "macOS-13.4-arm64-arm-64bit", "py_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "py_version_trio": "3.11.7", "answer": 1000000000, "answer_duration_ms": 1080.905433371663, "estimated_n": 10668767230, "bench_source": "chunk_size = 1_000_000  # 1 megabyte\ndata_chunk = \"a\" * chunk_size\noutput = StringIO()\nbytes_written = 0\nwhile bytes_written < n:\n    _ = output.write(data_chunk)\n    bytes_written += chunk_size\noutput.getvalue()", "bench_doc": "Number to guess: How many bytes can we write to a string in memory in a second?"}];
    const options = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000].map((n) => n.toLocaleString());
    let score = 0;
    let answered = 0;
    let unanswered = questions.length;
    function createQuiz() {
        const quizContainer = document.getElementById('quiz');
        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            const questionHeading = document.createElement('h3');
            questionHeading.textContent = question.name;
            questionDiv.appendChild(questionHeading);
            const questionText = document.createElement('p');
            questionText.textContent = question.bench_doc;
            questionDiv.appendChild(questionText);
            const questionPre = document.createElement('pre');
            const questionCode = document.createElement('code');
            questionPre.appendChild(questionCode);
            questionCode.textContent = question.bench_source;
            questionCode.classList.add('language-python');
            questionDiv.appendChild(questionPre);
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options';
            options.forEach(option => {
                const button = document.createElement('button');
                button.textContent = option;
                button.onclick = () => checkAnswer(button, question.answer, question.estimated_n, questionDiv);
                optionsDiv.appendChild(button);
            });
            questionDiv.appendChild(optionsDiv);
            quizContainer.appendChild(questionDiv);
        });
        document.getElementById('unanswered').textContent = unanswered;
    }
    function checkAnswer(button, correctAnswer, exactAnswer, questionDiv) {
        const allButtons = button.parentElement.children;
        for (let btn of allButtons) {
            btn.disabled = true;
            if (parseInt(btn.textContent.replace(/,/g, '')) === correctAnswer) {
                btn.classList.add('correct');
            }
        }
        if (parseInt(button.textContent.replace(/,/g, '')) !== correctAnswer) {
            button.classList.add('wrong');
        } else {
            score++;
            document.getElementById('score').textContent = score;
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
    createQuiz();
    hljs.highlightAll();
</script>
<!-- End Quiz -->




By studying napkin math, operating systems, and computer architecture I got a lot better at estimating
program performance.


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
</style>
