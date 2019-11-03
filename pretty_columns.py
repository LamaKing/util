#!/usr/bin/env python3

import sys, logging, argparse, io
from useful_functions import logger_setup, load_stream, adjust_col_width

def pretty_columns(argv):
    """Adjust the width of data lines in given file or stdin.

    Comment lines are start with given comment character.
    Comments can be grouped at the top or left at original position.

    Return stringIO with output (Python func) or prints on stdout (bash script)."""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=pretty_columns.__doc__,
                                     epilog="Silva 03-11-2019")
    # Positional arguments
    parser.add_argument('filename',
                        default=None,
                        type=str, nargs="?",
                        help='filename (if blank use stdin);')
    # Optional args
    parser.add_argument('--comment',
                        dest='comment_c', default="#",
                        help="""set comment character (use -1 for None).
                                NOTE: beware of the number of columns.""")
    parser.add_argument('--split',
                        action='store_true', dest='split_flg',
                        help='put comments at beginning of file;')
    parser.add_argument('--debug',
                        action='store_true', dest='debug',
                        help='show debug information.')

    #-------------------------------------------------------------------------------
    # Initialize and check variables
    #-------------------------------------------------------------------------------
    args = parser.parse_args(argv) # Process arguments

    # Set up logger and debug options
    c_log = logger_setup(__name__)
    c_log.setLevel(logging.INFO)
    debug_opt = [] # Pass debug flag down to other functions
    if args.debug:
        c_log.setLevel(logging.DEBUG)
        debug_opt = ['-d']
    c_log.debug(args)

    # Initialize input stream
    if args.filename is None:
        in_stream = sys.stdin
    else:
        in_stream = open(args.filename, 'r')

    if args.comment_c == "-1": args.comment_c = None

    #-------------------------------------------------------------------------------
    # Initialise output string stream
    #-------------------------------------------------------------------------------
    output = io.StringIO()

    #-------------------------------------------------------------------------------
    # Process stream
    #-------------------------------------------------------------------------------
    if args.split_flg:
        # Split comments and data
        c_log.debug("Splitting")
        comments, data = load_stream(in_stream, comment_char=args.comment_c)
        c_log.debug(comments)

        for l in comments+adjust_col_width(data):
            print(l, file=output)
    else:
        c_log.debug("Keep order")
        # Keep ordered
        c_num, data = load_stream(in_stream, comment_char=args.comment_c,
                                  split=False)
        c_log.debug(c_num)
        c_log.debug("Comments at "+"%i "*len(c_num), *c_num)
        # Adjust only data lines
        data_adj = adjust_col_width([l for i, l in enumerate(data)
                                     if i not in c_num] )
        for i, l in enumerate(data):
            if i in c_num:
                print(l, file=output)
            else:
                print(data_adj[i-len(c_num)], file=output)

    #-------------------------------------------------------------------------------
    # Close input and return output string stream
    #-------------------------------------------------------------------------------
    if args.filename: in_stream.close()
    return output

# If executed as bash script, execute function and print results
if __name__ == "__main__":
    # Last newling already included
    print(pretty_columns(sys.argv[1:]).getvalue(), end="")
