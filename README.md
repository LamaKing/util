# Util
Collection of useful script and Python modules

Ideally the util.py should be in your python path so you can import it easily.
A way to achieve this is to have a python start up script with a suitable command in it.
Create a file __.pythonrc__ in your home with these lines:
```
import sys, os
sys.path.append(os.getenv("HOME")+"/bin/")
``` 
And add the following to your __.bashrc__ file
```
export PYTHONSTARTUP="$HOME/.pythonrc"
```

To have the scripts as bash command, add this folder to the path or, probably better, link them to a folder which is in the path alread, e.g. ~/bin.
To implement the second solution use
```
ln -s /path/to/script.py /path/to/bin/
```
