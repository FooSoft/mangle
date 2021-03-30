# Install Instructions

For local development / building stand-alone binaries

You need Python 
[2.7 32 bit](https://www.python.org/downloads/release/python-2718/).

If you are using Windows download the `Windows x86 MSI installer`.

Be sure to add `python` to `PATH` during installation.

You can run `mangle` using 64 bit Python 2.7,
but won't be able to build a binary with `py2exe`,
and any performance difference is negligible.

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

You can run the GUI via

```
(venv) > python mangle.pyw
```

Optionally, you can install all the dependencies globally
so you can simply click on the `mangle.pyw` file to run it.

### Optional (Windows)

To actually build a stand-alone `.exe`, install
 
[Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

A standalone binary can be created in the `dist` folder via

```
(venv) > python setup.py install
```

You may get an error which can be solved by looking at
https://stackoverflow.com/questions/38444230/error-converting-gui-to-standalone-executable-using-py2exe
