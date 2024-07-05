---
layout: post
title: Computers are fast
date: 2024-07-4
summary: Do you know how much your computer can do in one second?
categories: performance programming modal
permalink: computers-are-fast
---

Let's find out how well you know computers!

All of these programs have a variable **`N`** in them. Your mission: guess how big **`N`** must get before the program takes 1 second to run.

You don't need to guess exactly. Just try to guess the right order of magnitude!
The options are all between one (10^0) and ten billion (10^10).

### But first, some introductory points

- If the answer is 38,400, both 10,000 and 100,000 are considered correct answers.
  The goal is to not be wrong by more than 10x, one order of magnitude 🤓.
- We know computers have different disk & network & CPU speeds! We're trying to understand the difference between code that can run ten times a second (10 Hz) and 100,000 times a second (100 KHz). A newer computer won't make any of the benchmark code run 1000x faster.
  - That said, the results are from running on an 2023 Mac M2 Max with Python 3.11.7 and rustc 1.78.0 (9b00956e5 2024-04-29).
- The Rust code was compiled with `--release`, of course.

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
    const pyQuestions = [{"name": "bench_loop", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 100000000, "answer_duration_ms": 984.858316599275, "estimated_n": 113003580, "bench_source": "for _ in range(n):\n\tpass", "bench_doc": "Number to guess: How many iterations of an empty loop can we go through in a second?", "hints": ["A CPU can execute around a few billion instructions per second."], "language": "python"}, {"name": "bench_dict_mutation", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10000000, "answer_duration_ms": 1005.4180583974812, "estimated_n": 30033836, "bench_source": "d = {}\nmax_entries = 1000\nfor i in range(n):\n\td[i % max_entries] = i", "bench_doc": "Number to guess: How many entries can we add to a dictionary in a second?", "hints": [], "language": "python"}, {"name": "bench_parse_http_request", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10000, "answer_duration_ms": 1002.374991599936, "estimated_n": 70082, "bench_source": "\tclass HTTPRequest(BaseHTTPRequestHandler):\n\t\tdef __init__(self, request_data: bytes):\n\t\t\tself.rfile = BytesIO(request_data)\n\t\t\tself.raw_requestline = self.rfile.readline()\n\t\t\tself.error_code = self.error_message = None\n\t\t\tself.parse_request()\n\n\t\tdef send_error(self, code, message):\n\t\t\tself.error_code = code\n\t\t\tself.error_message = message\n\n\trequest = b\"\"\"GET / HTTP/1.1\nHost: localhost:8001\nConnection: keep-alive\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\nAccept-Encoding: gzip, deflate, sdch\nAccept-Language: en-GB,en-US;q=0.8,en;q=0.6\n\"\"\"\n\tfor _ in range(n):\n\t\t_parsed = HTTPRequest(request)", "bench_doc": "Number to guess: How many HTTP GET requests can we parse in a second?", "hints": [], "language": "python"}, {"name": "bench_download_webpage", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 1, "answer_duration_ms": 791.2754165998194, "estimated_n": 3, "bench_source": "for _ in range(n):\n\tresponse = urllib.request.urlopen(\"http://google.com\")\n\tresponse.read()", "bench_doc": "Number to guess: How many times can we download google.com in a second?", "hints": ["This inefficiently establishes a new HTTP connection on each iteration"], "language": "python"}, {"name": "bench_run_python", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10, "answer_duration_ms": 857.6327999995556, "estimated_n": 74, "bench_source": "for _ in range(n):\n\tsubprocess.run(\"python3 -c ''\", shell=True, check=True)", "bench_doc": "Number to guess: How many times can we start the Python interpreter in a second?", "hints": ["This is much less than 100 million :)", "On startup Python reads of 100 files!", "Before running any code Python executes around 1000 syscalls"], "language": "python"}, {"name": "bench_create_files", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10000, "answer_duration_ms": 886.7174165992765, "estimated_n": 16530, "bench_source": "with tempfile.TemporaryDirectory() as temp_dir:\n\tfor i in range(n):\n\t\tfile_path = os.path.join(temp_dir, f\"{i}.txt\")\n\t\twith open(file_path, \"w\") as file:\n\t\t\tfile.flush()\n\t\t\tos.fsync(file.fileno())\n\t# Sync the directory to ensure the file metadata is written to disk\n\tdir_fd = os.open(temp_dir, os.O_RDONLY)\n\ttry:\n\t\tos.fsync(dir_fd)\n\tfinally:\n\t\tos.close(dir_fd)", "bench_doc": "How many fsync'd files can be created against an SSD in a second?", "hints": ["The fsync syscall per-file significantly impacts performance"], "language": "python"}, {"name": "bench_write_to_disk", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 1000000000, "answer_duration_ms": 996.3692584016826, "estimated_n": 4642374667, "bench_source": "def cleanup(f, name):\n\tf.flush()\n\tos.fsync(f.fileno())\n\tf.close()\n\ttry:\n\t\tos.remove(name)\n\texcept OSError:\n\t\tpass\n\nchunk_size = 1_000_000  # 1 megabyte\ndata_chunk = b\"a\" * chunk_size\nname = \"/tmp/bench-write-to-disk\"\nbytes_written = 0\nwith open(name, 'wb') as f:\n\twhile bytes_written < n:\n\t\twritten = f.write(data_chunk)\n\t\tbytes_written += chunk_size\n\t\tassert written == chunk_size, \"incomplete disk write\"\n\tcleanup(f, name)", "bench_doc": "Number to guess: How many bytes can we write to an output file in a second?", "hints": ["We make sure everything is sync'd to disk before exiting"], "language": "python"}, {"name": "bench_write_to_memory", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 1000000000, "answer_duration_ms": 1102.3937333986396, "estimated_n": 9306062376, "bench_source": "chunk_size = 1_000_000  # 1 megabyte\ndata_chunk = \"a\" * chunk_size\noutput = StringIO()\nbytes_written = 0\nwhile bytes_written < n:\n\t_ = output.write(data_chunk)\n\tbytes_written += chunk_size\noutput.getvalue()", "bench_doc": "Number to guess: How many bytes can we write to a string in memory in a second?", "hints": [], "language": "python"}, {"name": "bench_json_parse", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 1000, "answer_duration_ms": 1000.4698916018242, "estimated_n": 4058, "bench_source": "# NB: reading the 64KiB file is a small constant overhead on each run.\ndata = pathlib.Path(\"message.json\").read_text()\nfor _ in range(n):\n\tjson.loads(data)", "bench_doc": "Number to guess: parse iterations possible within one second. File size is 64KiB.", "hints": [], "language": "python"}, {"name": "bench_sha256_digest", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 100000000, "answer_duration_ms": 998.9452416019049, "estimated_n": 597359817, "bench_source": "CHUNK_SIZE = 10_000\ns = b'a' * CHUNK_SIZE\nh = hashlib.md5()\nbytes_hashed = 0\nwhile bytes_hashed < n:\n\th.update(s)\n\tbytes_hashed += CHUNK_SIZE\nh.digest()", "bench_doc": "Number to guess: bytes hashed in one second.", "hints": ["sha256 is cryptographically secure and slower than md5, siphash, CRC32."], "language": "python"}, {"name": "bench_fill_array", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10000000, "answer_duration_ms": 1009.9795418005671, "estimated_n": 39230461, "bench_source": "array = bytearray(n)\nfor i in range(n):\n\tarray[i] = i % 256  # Ensure value fits in a byte\nprint(array[n // 7], end='')", "bench_doc": "Number to guess: bytes written to array in one second.", "hints": [], "language": "python"}, {"name": "bench_fill_array_out_of_order", "platform": "macOS-13.4-arm64-arm-64bit", "lang_version": "3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)]", "answer": 10000000, "answer_duration_ms": 1012.7391250018263, "estimated_n": 15155037, "bench_source": "array = bytearray(n)\njmp_around = 1\nfor _ in range(n):\n\tjmp_around = jmp_around * 2\n\tif jmp_around > n:\n\t\tjmp_around -= n\n\tarray[jmp_around % n] = jmp_around % 256  # Ensure index and value fit in range\n\nprint(array[n // 7])", "bench_doc": "Number to guess: bytes written to array in one second.", "hints": [], "language": "python"}];
    const rustQuestions = [{"name":"bench_loop","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":298.0,"estimated_n":3355704697,"bench_source":"for _ in 0..n {\n\tblack_box(());\n}","bench_doc":" Number to guess: How many iterations of an empty loop can we go through in a second?","hints":["black_box(()) is used only to avoid compiler optimizing out the loop. It adds no run time overhead.","A CPU can execute around a few billion instructions per second."],"language":"rust"},{"name":"bench_dict_mutation","platform":"Darwin-13.4-arm64","lang_version":"","answer":100000000,"answer_duration_ms":803.0,"estimated_n":124533001,"bench_source":"let mut m = HashMap::new();\nlet max_entries = 1000;\nfor i in 0..n {\n\tm.insert(i % max_entries, i);\n}","bench_doc":" Number to guess: How many entries can we add to a std::HashMap in a second?","hints":null,"language":"rust"},{"name":"bench_download_webpage","platform":"Darwin-13.4-arm64","lang_version":"","answer":1,"answer_duration_ms":111.0,"estimated_n":9,"bench_source":"for _ in 0..n {\n\tlet mut stream = TcpStream::connect(\"google.com:80\").unwrap();\n\tlet request = \"GET / HTTP/1.1\\r\\nHost: google.com\\r\\nConnection: close\\r\\n\\r\\n\";\n\tstream.write_all(request.as_bytes()).unwrap();\n\tlet mut response = String::new();\n\tstream.read_to_string(&mut response).unwrap();\n}","bench_doc":" Number to guess: How many times can we download google.com in a second?","hints":null,"language":"rust"},{"name":"bench_run_python","platform":"Darwin-13.4-arm64","lang_version":"","answer":10,"answer_duration_ms":104.0,"estimated_n":96,"bench_source":"for _ in 0..n {\n\tlet mut child = std::process::Command::new(\"python3\")\n\t\t.args([\"-c\", \"''\"])\n\t\t.spawn()\n\t\t.expect(\"failed to execute child\");\n\tlet ecode = child.wait().expect(\"failed to wait on child\");\n\tassert!(ecode.success());\n}","bench_doc":" Number to guess: How many times can we start the Python interpreter in a second?","hints":["This is much less than 100 million :)","On startup Python reads of 100 files!","Before running any code Python executes around 1000 syscalls"],"language":"rust"},{"name":"bench_create_files","platform":"Darwin-13.4-arm64","lang_version":"","answer":100,"answer_duration_ms":454.0,"estimated_n":220,"bench_source":"let dir = tempdir().unwrap();\nfor i in 0..n {\n\tlet file_path = dir.path().join(format!(\"{}.txt\", i));\n\tlet file = File::create(file_path).unwrap();\n\tfile.sync_all().unwrap();\n}\nlet dir_path = dir.path();\nlet dir_file = OpenOptions::new().read(true).open(dir_path).unwrap();\ndir_file.sync_all().unwrap();","bench_doc":" Number to guess: How many fsync'd files can be created against an SSD in a second?","hints":null,"language":"rust"},{"name":"bench_write_to_disk","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":442.0,"estimated_n":2262443438,"bench_source":"const CHUNK_SIZE: usize = 1_000_000;\nlet data_chunk: [u8; CHUNK_SIZE] = [b'a'; CHUNK_SIZE];\nlet mut f = std::fs::File::create(\"/tmp/bench-write-to-disk\").unwrap();\nlet mut bytes_written = 0;\nwhile bytes_written < n {\n\tlet written = f.write(&data_chunk).unwrap();\n\tbytes_written += CHUNK_SIZE as u64;\n\tassert_eq!(written, CHUNK_SIZE, \"incomplete disk write\");\n}\nf.sync_all().unwrap();","bench_doc":" Number to guess: How many bytes can we write to an output file in a second?","hints":["We make sure everything is sync'd to disk before exiting"],"language":"rust"},{"name":"bench_write_to_memory","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000000000,"answer_duration_ms":125.0,"estimated_n":8000000000,"bench_source":"const CHUNK_SIZE: usize = 1_000_000;\nlet data_chunk: [u8; CHUNK_SIZE] = [b'a'; CHUNK_SIZE];\nlet mut buffer: Vec<u8> = vec![];\nlet mut bytes_written = 0;\nwhile bytes_written < n {\n\tbuffer.extend(&data_chunk);\n\tbytes_written += CHUNK_SIZE as u64;\n}\nassert!(buffer.len() >= n as usize);","bench_doc":" Number to guess: How many bytes can we write to a string in memory in a second?","hints":null,"language":"rust"},{"name":"bench_json_parse","platform":"Darwin-13.4-arm64","lang_version":"","answer":1000,"answer_duration_ms":267.0,"estimated_n":3745,"bench_source":"let data = std::fs::read_to_string(\"message.json\").unwrap();\nfor _ in 0..n {\n\tlet _json: serde_json::Value = serde_json::from_str(&data).unwrap();\n}","bench_doc":" Number to guess: parse iterations possible within one second. File size is 64KiB.","hints":null,"language":"rust"},{"name":"bench_sha256_digest","platform":"Darwin-13.4-arm64","lang_version":"","answer":100000000,"answer_duration_ms":276.0,"estimated_n":362318840,"bench_source":"use sha2::{Digest, Sha256};\nconst CHUNK_SIZE: usize = 10_000;\nlet s = \"a\".repeat(CHUNK_SIZE);\nlet mut bytes_hashed: usize = 0;\nlet mut h = Sha256::new();\nwhile bytes_hashed < (n as usize) {\n\th.update(s.as_bytes());\n\tbytes_hashed += CHUNK_SIZE;\n}\nh.finalize();","bench_doc":" Number to guess: bytes hashed in one second.","hints":["sha256 is cryptographically secure and slower than md5, siphash, CRC32."],"language":"rust"},{"name":"bench_fill_array","platform":"Darwin-13.4-arm64","lang_version":"","answer":100000000,"answer_duration_ms":130.0,"estimated_n":769230769,"bench_source":"let n: usize = n as usize;\nlet mut a = vec![0u8; n];\nlet mut j: usize = 1;\nfor i in 0..n {\n\tj *= 2;\n\tif j > n {\n\t\tj -= n;\n\t}\n\ta[i] = (j % 256) as u8;\n}\nprintln!(\"{}\", a[n / 7]);","bench_doc":" Number to guess: bytes written to array in one second.","hints":null,"language":"rust"},{"name":"bench_fill_array_out_of_order","platform":"Darwin-13.4-arm64","lang_version":"","answer":100000000,"answer_duration_ms":548.0,"estimated_n":182481751,"bench_source":"let n: usize = n as usize;\nlet mut a = vec![0u8; n];\nlet mut jump_around: usize = 1;\nfor _ in 0..n {\n\tjump_around *= 2;\n\tif jump_around > n {\n\t\tjump_around -= n;\n\t}\n\ta[jump_around % n] = (jump_around % 256) as u8;\n}\nprintln!(\"{}\", a[n / 7]);","bench_doc":" Number to guess: bytes written to array in one second.","hints":null,"language":"rust"}];
    const options = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000].map((n) => n.toLocaleString());
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
        <br>
        <p>
            If you want to improve your performance estimation skills I'd recommend checking out <a href="https://teachyourselfcs.com/">teachyourselfcs.com</a> and <a href="https://github.com/sirupsen/napkin-math">sirupsen/napkin-math</a>.
        </p>
    </div>
</div>

<style>
    #quiz pre {
        tab-size: 4;
    }

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
