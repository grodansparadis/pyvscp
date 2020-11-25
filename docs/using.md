# Using the library

There is a sample [here](https://github.com/grodansparadis/pyvscp/tree/main/tests) that uses most of the methods available in the library. 

There are some other libraries that usually is used together with this library.

* [pyvscphelper](https://github.com/grodansparadis/pyvscphelper). The vscp helper library has many functions for different VSCP and general tasks. **pyvscphelp** is the official Python helper library for VSCP & friends. It builds on the C helper library that has been available from the beginning of VSCP development. The library is normally used together with 
* [pyvscpclasses](https://github.com/grodansparadis/pyvscpclasses). The vscp_class library contains VSCP class definitions. 
* [pyvscptypes](https://github.com/grodansparadis/pyvscptypes). The vscp_type library contains VSCP type definitions. 

There are also other Python related VSCP libraries and you find a list [here](https://github.com/search?q=user%3Agrodansparadis+pyvscp)


## Install on Linux

The pyvscp module is available on PyPi. Install it from PyPi is the easiest way to obtain the module. To install it on your machine use

```bash
pip3 install pyvscp
```
To install in a virtual environment in your current project:

```bash
mkdir project-name && cd project-name
python3 -m venv .env
source .env/bin/activate
pip3 install pyvscp
```

Upgrade with

```bash
pip3 install --upgrade pyvscp
```


## Install on Windows

On windows run 

```bash
cmd
```

as administrator and use

```bash
python -m pip install pyvscp
```

to install the library.

On GitHub you can find the code at (https://github.com/grodansparadis/pyvscp)


## To use in a (new) project

```python
import vscp 
```

is the standard way to im,port the library. This means that you have to prefix every function in the library with "vscp". An optional import method is

```python
from vscp import *
```
which makes it possible ti use the library resources without a prefix. Using the first method is recommended.

[filename](./bottom_copyright.md ':include')