#!/usr/bin/env python3

import sys
import os, argparse, logging
from ase.io.vasp import read_vasp_xdatcar
from ase.io.extxyz import write_xyz

def xdatcar_to_xyz(argv):
    """Convert XDATCAR file to xyz.

    Each comment line begins with #.
    After frame number is printed. If timestep is given, actual time is written; assumes fs.
    First comment line contains ASE object info as well.

    Result is written on stdout."""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=__doc__)
    # Positional arguments
    parser.add_argument('filename',
                        default='XDATCAR',
                        type=str, nargs='?',
                        help='input file. If not given XDATCAR is used;') # if NULL is given, stdin is used.')
    # Optional args
    parser.add_argument('--dt',
                        dest='dt', type=float, default=None,
                        help='timestep in femptosecon;')
    parser.add_argument('--debug',
                        action='store_true', dest='debug',
                        help='show debug informations.')

    #-------------------------------------------------------------------------------
    # Initialize and check variables
    #-------------------------------------------------------------------------------
    args = parser.parse_args(argv)

    # Set up LOGGER
    c_log = logging.getLogger(__name__)
    # Adopted format: level - current function name - mess. Width is fixed as visual aid
    std_format = '[%(levelname)5s - %(funcName)10s] %(message)s'
    logging.basicConfig(format=std_format)
    c_log.setLevel(logging.INFO)
    # Set debug option
    if args.debug: c_log.setLevel(logging.DEBUG)

    c_log.debug(args)

    # Set time variable properly
    t_unit = "fs"
    if args.dt is None:
        args.dt = 1
        t_unit = ""

    #-------------------------------------------------------------------------------
    # Load file and print xyz to stdout
    #-------------------------------------------------------------------------------
    # Load xdatcar as list of Atoms obj
    # For some reason we need to put index=0 to load all of it, otherwise is just the first.
    for t, frame in enumerate(read_vasp_xdatcar(args.filename, index=0)):
        c_line = "# %.6f %s " % (t*args.dt, t_unit)
        # If it's the first line, print first atoms object info
        # Here we are assuming that since it's MD, cell and compositions are not changing.
        if t == 0:
            c_line += "%s %s" % (frame, frame.info)

        write_xyz(sys.stdout, frame, append=True,
                  comment=c_line)
# If executed as bash script, execute function and return exit status to bash
if __name__ == "__main__":
    # From https://github.com/python/mypy/issues/2893
    # "Python interpreter [...] overrides the default handling of SIGPIPE; specifically, it ignores this signal."
    # Restore it to the default handler, SIG_DFL
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    xdatcar_to_xyz(sys.argv[1:])
