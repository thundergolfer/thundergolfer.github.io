---
layout:     post
title:      A Basic Python Toolchain in Bazel 
date:       2021-06-25
summary:    How to improve on the default auto-detecting Python toolchain shipped with Bazel. 
categories: bazel python
---

<div class="callout-panel callout-panel-warning">
    <span class="callout-panel-icon callout-panel-warning-icon">
        <span class="" role="img" aria-label="Panel warning">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <g fill-rule="evenodd"><path d="M12.938 4.967c-.518-.978-1.36-.974-1.876 0L3.938 18.425c-.518.978-.045 1.771 1.057 1.771h14.01c1.102 0 1.573-.797 1.057-1.771L12.938 4.967z" fill="currentColor"></path><path d="M12 15a1 1 0 0 1-1-1V9a1 1 0 0 1 2 0v5a1 1 0 0 1-1 1m0 3a1 1 0 0 1 0-2 1 1 0 0 1 0 2" fill="inherit"></path></g>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            This toolchain was banged together very quickly and isn't thorough reviewed or tested. Treat the following content as educational and possibly helpful in setting up your own toolchain solution and not as a 'ready-made' toolchain.
        </p>
    </div>
</div>

----

Here's how to quickly setup a basic hermetic Python toolchain in Bazel. The default Bazel toolchain used in [bazelbuild/**rules_python**](https://github.com/bazelbuild/rules_python) 
is the 'autodetecting toolchain', called `@bazel_tools//tools/python:_autodetecting_py_runtime_pair`. You probably don't want to 
use it, as it is completely non-hermetic and leads to a number of frustrating user issues. Quite a few Github issues created on 
the rules_python project can be traced back to this default leaky setup. It is non-hermetic because the auto-detecting toolchain 
looks for the Python interpreter on your `$PATH`. Your path includes the system Python, anything stuck in there by Homebrew or PyEnv, 
and god knows what else. You want to get Bazel to use a hermetic Python toolchain, a toolchain that is closed off and leaves the 
interpreter strictly versioned and protected from unwanted interference. Let's try for that.

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
            If you don't know what a Bazel toolchain is and how it's useful, spend 15 minutes reading through <a href="https://docs.bazel.build/versions/main/toolchains.html">docs.bazel.build - Toolchains</a>
        </p>
    </div>
</div>

At work we use Nix and Nixpkgs to pull in a hermetic toolchain, but offering Nix as a solution to people already wrestling with the complex Bazel system is just cruel. Nix is too much. It's a full reproducible package building ecosystem and our problem is just to setup a single Python interpreter that can install packages and run programs and lets us get back to writing application code that makes our users happy. 

This basic toolchain setup just involves:

1. **Using Starlark to download a Python interpreter:** a bit of custom Starlark to download and unpack a standalone Python interpreter.gi
2. **Defining the toolchain:** a `BUILD.bazel` file to define our a `py_runtime` and pass it into Bazel's `toolchain` setup rule.
3. **Registering the toolchain:** the registration of this new toolchain with Bazel's toolchain resolution system.


I have defined the custom Starlark `.bzl` module and the `BUILD` file in the same Bazel package: `//tools/build/bazel/py_toolchain`.  So we'll have:

- `tools/build/bazel/py_toolchain/py_interpreter.bzl`
- `tools/build/bazel/py_toolchain/BUILD.bazel`

## Warning: Missing hermeticity

<div class="callout-panel callout-panel-warning">
    <span class="callout-panel-icon callout-panel-warning-icon">
        <span class="" role="img" aria-label="Panel warning">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <g fill-rule="evenodd"><path d="M12.938 4.967c-.518-.978-1.36-.974-1.876 0L3.938 18.425c-.518.978-.045 1.771 1.057 1.771h14.01c1.102 0 1.573-.797 1.057-1.771L12.938 4.967z" fill="currentColor"></path><path d="M12 15a1 1 0 0 1-1-1V9a1 1 0 0 1 2 0v5a1 1 0 0 1-1 1m0 3a1 1 0 0 1 0-2 1 1 0 0 1 0 2" fill="inherit"></path></g>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            The standalone Python interpreter is downloaded in the "zstd" compression format, and thus you'll need to have the <code>zstd</code> binary already present on the machine running Bazel. This is annoying, and certainly not a Bazel best-practice. I think the most obvious improvement to the situation would be to host pre-built binaries of <code>zstd</code> and download them during the repository rule's execution.
        </p>
    </div>
</div>

## Using Starlark to download a Python interpreter

The `py_interpreter.bzl` module will define a repository rule that executes at WORKSPACE evaluation time to produce an external Bazel repository with two Bazel targets:

1. `:interpreter` - a 'filegroup' rule exposing a single file, the executable interpreter binary.
2. `:files` - also a 'filegroup' rule, containing a bunch of files that a needed by the interpreter, such as C header files, the stdlib modules, and other stuff.

These get used to create a `py_runtime` target, which is a special Bazel rule that "Represents a Python runtime used to execute Python code."

The Python distribution we'll download is released by Gregoy Szorc under the **[python-build-standalone](https://python-build-standalone.readthedocs.io/en/latest/)** project. The project releases "self-contained, highly-portable Python distributions" which sounds perfectly suitable for us as a download-and-run hermetic Python toolchain.

The high-level logic of the repository rule is as follow:

1. Figure out what OS platform we're running on and if the rule supports it.
2. If yes, fetch a python-build-standalone distribution and unpack it into an external Bazel repository created by the instantiation of our named repository rule. 
3. Create a `BUILD.bazel` file with the `:interpreter` and `:files` targets so that the files sitting in that external repository can be used in the `WORKSPACE`.

Pretty simple. Without further ado, here's the module:

```python
# py_interpreter.bzl
OSX_OS_NAME = "mac os x"
LINUX_OS_NAME = "linux"

def _python_build_standalone_interpreter_impl(repository_ctx):
    os_name = repository_ctx.os.name.lower()

    # TODO(Jonathon): This can't differentiate ARM (Mac M1) from old x86.
    # TODO(Jonathon: Support Windows.
    if os_name == OSX_OS_NAME:
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-apple-darwin-pgo+lto-20210228T1503.tar.zst"
        integrity_shasum = "4c859311dfd677e4a67a2c590ff39040e76b97b8be43ef236e3c924bff4c67d2"
    elif os_name == LINUX_OS_NAME:
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20210228/cpython-3.8.8-x86_64-unknown-linux-gnu-pgo+lto-20210228T1503.tar.zst"
        integrity_shasum = "74c9067b363758e501434a02af87047de46085148e673547214526da6e2b2155"
    else:
        fail("OS '{}' is not supported.".format(os_name))

    # TODO(Jonathon): Just use download_and_extract when it supports zstd. https://github.com/bazelbuild/bazel/pull/11968
    repository_ctx.download(
        url = [url],
        sha256 = integrity_shasum,
        output = "python.tar.zst",
    )

    # TODO(Jonathon): NOT HERMETIC. Need to install 'unzstd' in rule and use it.
    unzstd_bin_path = repository_ctx.which("unzstd")
    if unzstd_bin_path == None:
        fail("On OSX and Linux this Python toolchain requires that the zstd and unzstd exes are available on the $PATH, but it was not found.")

    # NOTE: *Not Hermetic*. Need to install 'unzstd' in rule and use it.
    res = repository_ctx.execute([unzstd_bin_path, "python.tar.zst"])

    if res.return_code:
        fail("Error decompressing with zstd" + res.stdout + res.stderr)

    repository_ctx.extract(archive = "python.tar")
    repository_ctx.delete("python.tar")
    repository_ctx.delete("python.tar.zst")

    # NOTE: 'json' library is only available in Bazel 4.*.
    python_build_data = json.decode(repository_ctx.read("python/PYTHON.json"))

    BUILD_FILE_CONTENT = """
filegroup(
    name = "files",
    srcs = glob(["install/**"], exclude = ["**/* *"]),
    visibility = ["//visibility:public"],
)

filegroup(
    name = "interpreter",
    srcs = ["python/{interpreter_path}"],
    visibility = ["//visibility:public"],
)
""".format(interpreter_path = python_build_data["python_exe"])

    repository_ctx.file("BUILD.bazel", BUILD_FILE_CONTENT)
    return None

python_build_standalone_interpreter = repository_rule(
    implementation = _python_build_standalone_interpreter_impl,
    attrs = {},
)
```

## Defining the toolchain

Now that we have the two new targets we can set up the build targets that fulfil the Python toolchain contract.

```python
# BUILD.bazel
load("@rules_python//python:defs.bzl", "py_runtime_pair")

py_runtime(
    name = "python3_runtime",
    files = ["@python_interpreter//:files"],
    interpreter = "@python_interpreter//:interpreter",
    python_version = "PY3",
    visibility = ["//visibility:public"],
)

py_runtime_pair(
    name = "py_runtime",
    py2_runtime = None,
    py3_runtime = ":python3_runtime",
)

toolchain(
    name = "py_toolchain",
    toolchain = ":py_runtime",
    toolchain_type = "@bazel_tools//tools/python:toolchain_type",
)
```

## Register the toolchain

The final step is to instantiate the interpreter and register our new toolchain in the `WORKSPACE` file. 

```python
# WORKSPACE
load("//tools/build/bazel/py_toolchain:py_interpreter.bzl", "python_build_standalone_interpreter")

python_build_standalone_interpreter(
    name = "python_interpreter",
)

register_toolchains("//tools/build/bazel/py_toolchain:py_toolchain")
```

After doing this, our toolchain will be used in all `py_*` targets. If you use the `rules_python` project's `pip_install` 
rule you should also use the `python_interpreter_target` attribute to have the interpreter used in package installation be identical 
to your build target intepreter: 

```python
# WORKSPACE
pip_install(
   name = "pypi",
   requirements = "//:requirements.txt",
   python_interpreter_target = "@python_interpreter//:python/install/bin/python3.8"
)
```

Note that this has to reference the specific Python interpreter file, not the `filegroup` target, and that's a little janky, 
but it's the best option we've got.

## Done

With that all set up, I'm able to install packages like `numpy` and `pytorch` to use them in a `py_binary` target, with 
everything using the Python 3.8.8 interpreter defined in our toolchain. It's a decent start.

I'm currently test-driving this in the [github.com/thundergolfer/**example-bazel-monorepo**](https://github.com/thundergolfer/example-bazel-monorepo) repository if you want to try it out.


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
