# Install Instructions

For local development / building stand-alone binaries.

You need [Python 2.7](https://www.python.org/downloads/release/python-2718/).

If you are using Windows 
and want to build a stand-alone binary 
download the `Windows x86 MSI installer`
because `py2exe` for Python 2 doesn't work with 64 bit.
Any performance increase from 64 bit is negligible.

Be sure to add `python` to `PATH` during installation.

Install [virtualenv](https://virtualenv.pypa.io/en/stable/) 
globally, if you don't already have it.

```
> pip install virtualenv
```

and install all dependencies in a venv in the mangle directory, e.g.

```
...\mangle> virtualenv venv
> venv\Scripts\activate
(venv) > pip install -r requirements.txt
```

You can run the app via

```
(venv) > python mangle.pyw
```

Optionally, you can install all the dependencies globally
so you can simply click on the `mangle.pyw` file to run it.

# Building an Executable (Windows)

To actually build a stand-alone `.exe`, install
 
[Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

A standalone binary can be created in the `dist` folder via

```
(venv) > python setup.py
```

You may get an error which can be solved by looking at
https://stackoverflow.com/questions/38444230/error-converting-gui-to-standalone-executable-using-py2exe
