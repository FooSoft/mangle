# Install Instructions

For local development / building stand-alone binaries

## Windows

You need Python 
[2.7 32 bit](https://www.python.org/downloads/release/python-2718/).
Download the `Windows x86 MSI installer` 
and be sure to add `python` to `PATH` during installation.

You can run `mangle` using 64 bit Python 2.7,
but won't be able to build a binary with `py2exe`,
and any performance difference is negligible.

Install virtualenv globally, if you don't already have it.

```
> pip install virtualenv
```

and install all dependencies in a venv in the mangle directory, e.g.

```
...\mangle> virtualenv venv
> venv\Scripts\activate
(venv) > pip install Pillow
(venv) > pip install reportlab
```

It can be pretty difficult to install PyQT4 from source,
so prebuilt binaries are available at
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

You need 
`PyQt4-4.11.4-cp27-cp27m-win32.whl`

which you can install after placing the file
in the `mangle` folder via

```
(venv) > pip install PyQt4-4.11.4-cp27-cp27m-win32.whl
```

So your final `pip freeze` can look like:

```
(venv) > pip freeze
Pillow==6.2.2
PyQt4 @ file:///.../mangle/PyQt4-4.11.4-cp27-cp27m-win32.whl
reportlab==3.5.59
```

You can run the GUI via

```
(venv) > python mangle.pyw
```

Optionally, you can install all the dependencies globally
so you can simply click on the `mangle.pyw` file to run it.

### Optional

To actually build a stand-alone `.exe`, install

```
(venv) > pip install py2exe_py2
```

and install 
[Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

A standalone binary can be created in the `dist` folder via

```
(venv) > python setup.py install
```

You may get an error which can be solved by looking at
https://stackoverflow.com/questions/38444230/error-converting-gui-to-standalone-executable-using-py2exe
