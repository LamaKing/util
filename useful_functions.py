"""
--------------------------------
 GENERAL-PORPOUSE FUNCTIONS
--------------------------------

A collection of often-used functions:
 - code shortcuts;
 - smart file readers;
 - string formatter;
 - container manipulators;

Python 3 only.

Created:    Silva 29-01-2018
Last edit:  Silva 03-11-2019
"""

import collections
import logging

#------------------------------------------------------------------------------#
# Bash-like script setup shortcuts
#------------------------------------------------------------------------------#

def logger_setup(module_name):
    """Set up standar logger for a module and return it"""

    # Set up LOGGER
    c_log = logging.getLogger(module_name) # Use name of the calling moduel, not this function
    # Adopted format: level - current function name - mess. Width is fixed as visual aid
    std_format = '[%(levelname)5s - %(funcName)10s] %(message)s'
    logging.basicConfig(format=std_format)
    # Logging level is defined by calling module via root logger
    return c_log

#------------------------------------------------------------------------------#
# Shortcut
#------------------------------------------------------------------------------#

def list2str(listarg, sep=' '):
    """Create a string out of a list with given separator (def=space)"""
    sep = str(sep)
    return sep.join(lmap(str, listarg))

def lmap(func, listarg):
    """Map given function to given list and return a list instead of iterator"""
    return list(map(func, listarg))

#------------------------------------------------------------------------------#
# Read files smartly
#------------------------------------------------------------------------------#
# Load data (comments+data)
# Should rename to split_stream
def load_stream(stream, comment_char="#", f=lambda x: x, split=True):
    """Load given stream object.

    Divide lines between comments (default char=#) and data, each divided in its fields.

    A function f can be given given as input and applied to each non-comment field.

    Accoring to split flag:
    - True (default): return tuple (comments, data)
                      Comment lines l are return as "<comment_char><line number>:l".
    - False: return tuple (coment indices, ordered field-split data and comment)

    Not suitable for big files: all content loaded."""

    stream_lines = stream.readlines()

    # Read the input file and filter the bash-like comments
    # Split comments and data in sparate objects
    if split:
        comments = [(comment_char+"%i:"%i) + l[1:].strip()
                    for i, l in enumerate(stream_lines)
                    if l.strip()[0] == comment_char]
        data = [[f(x) for x in l.strip().split()]
                for l in stream_lines
                if l.strip()[0] != comment_char]
        return comments, data

    # Return comment lines number and ordered list of comments and data lines
    comment_lnum = []
    data = []
    for i, l in enumerate(stream_lines):
        l = l.strip()
        if l[0] == comment_char:
            comment_lnum.append(i)
            data.append(l)
        else:
            data.append([f(x) for x in l.split()])

    return comment_lnum, data

def load_file(filename, comment_char="#"):
    """Load given filename.

    Divide lines between comments and data.
    Comment char can be given as input."""
    with open(filename, 'r') as in_file:
        return load_stream(in_file, comment_char)

def load_float_file(filename, comment_char="#"):
    """Load given numeric filename.

    Each non-comment field will be cast to float and the whole stream in NumPy array.
    Divide lines between comments and data.
    Not suitable for big files."""
    import numpy as np
    with open(filename, 'r') as in_file:
        # Appreciate the power of **kwarg expansion!
        c, d = load_stream(in_file, **{"comment_char" : comment_char, "f": float})
        d = np.array(d)
        return c, d

#------------------------------------------------------------------------------#
# String formatting
#------------------------------------------------------------------------------#

def set_width(args, w=None, align_char="<", offset=2):
    """Set the width of given list

    Width can be an int (applied to all args) a list of width (one per argument).
    If width is not given a the maximum length of the args + offset is used.

    The alignment can be specified giving the proper formatting characher:
    - "<" for left align (default)
    - "^" for centred
    - ">" for right
    """

    # Check aligmnet is valid
    if align_char not in ["<", "^", ">"]:
        raise ValueError("Alignment char must be left (<), center (^) or right (>), not",
                         align_char)
    # Define template format string
    tmpl_format = "{:"+align_char+"{width}}"

    # Converte all fields to string. You're never safe enough
    args = list(map(str, args))

    # Width mode: single, list, auto
    if isinstance(w, int):
        # --> Single value for all
        w_args = [w]*len(args)
    elif isinstance(w, list):
        # --> Specific width per each arg
        if False in [isinstance(wi, int) for wi in w]:
            raise ValueError("Width of each char must be int")
        if len(w) != len(args):
            raise ValueError("Width and args must have same length")
        w_args = w
    elif w is None:
        # Auto: compute a reasonable estimation from arguments.
        w_args = [offset + max([len(s.strip()) for s in args])]*len(args)
    else:
        raise ValueError("Width style not recognised")

    # Run over args and relative width, put them in format string and join all.
    return "".join([tmpl_format.format(s, width=w)
                    for s, w in zip(args, w_args)]
                  )

def adjust_col_width(rows, align_char="<", offset=5):
    """Set width of a n-list of m-list to (max + offset) of each column

    Structure assumed is list of rows: [ [1, 2, ..., m], [1,2,...,m], ..., n]
    Returns a n-list of  strings.
    """

    # Get dimension m of the rows (first must be equal to all others)
    cols_w =  [0]*len(rows[0])
    # Check input and compute right width
    for i, ri in enumerate(rows):
        if len(ri) != len(cols_w):
            raise ValueError("All lines must have same length")
        # To be sure, convert to string
        ri = lmap(str, ri)
        rows[i] = ri
        # Loop on fields
        for j, field in enumerate(ri):
            w_f = len(field) # Current field width
            # If longer than current value, update
            if w_f > cols_w[j]:
                cols_w[j] = w_f

    # Apply width offset to computed width and set width of each row
    return [set_width(r, [w+offset for w in cols_w], align_char=align_char)
            for r in rows]

def set_float_width(args, w=None, align_char="<", offset=2, prec=15):
    """Set convert list of float to string and set width

    Set precision of conversion with "prec" keyword.
    Then pass the converted floats to set_width function
    """

    # Converte all fields to string.
    conv_tmpl= "%"+"%i.%i" % (prec+5, prec)+"f"
    args = [conv_tmpl % n for n in args ]
    return set_width(args, w=w, align_char=align_char, offset=offset)

#------------------------------------------------------------------------------#
# Lists manipulators
#------------------------------------------------------------------------------#

# Nice recursive, yield-wise flatten function
def flatten(l):
    """Flat list generator from nested lists"""
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

# Lazy way of do it...
def lflatten(l):
    """Flat list from a nested one"""
    return  list(flatten(l))

def list_uniq(l):
    """List of uniq elements in given list l.
    Preserves original order, differently than set."""
    seen = set()
    seen_add = seen.add # Faster than evaulating seen.add at each iter
    return [x for x in l if not (x in seen or seen_add(x))]
