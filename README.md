# SimplePythonInterpreter
A simple interpreter built with python

# How to use
You need to have python3 installed.
Install the `ply` library:
```
pip install ply
```
You can run your presonal scripts using the following command:
```
python main.py path/to/yout/sctipt.mini
```
Where `path/to/your/scirpt.mini` is the path of the file that you want to run.

# Examples

Check the scripts in the `tests` folder.
- `test1-server.mini`: a program that executes a local server that listens to connections. This server will recieve a mathematical operation and will return the result to the client connected to it.
- `test1-client.mini`: this program connects to the server and sends a mathematical expression and recieves the result from the server.
- `test2.mini`: this program uses the builtins function for Fibonacci and factoral and executes them parallely.
- `test3.mini`: the same as `test2.mini` but doesn't uses the builtin functions.  
