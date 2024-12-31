# py_limit_memory
constrain/limit the memory (RAM) of a process in python for a function via a function decorator on linux

## Install
first clone or download the repo and use pip to install
```shell
git clone https://github.com/drnhhl/py_limit_memory
cd py_limit_memory
pip install .
```

## Usage
```python
from py_limit_memory import limit_memory

@limit_memory("10GB") # limit to 10GB
def function_to_limit():
    pass

# or

@limit_memory("10%") # limit to 10% of the total RAM
def function_to_limit():
    pass
```

## Credit
code adapted from: [stackoverflow](https://stackoverflow.com/questions/41105733/limit-ram-usage-to-python-program)
