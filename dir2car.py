#!/usr/bin/env python3

import sys
import os, argparse, logging
import ase.io
from ase.build import sort as ase_sort

def dir2car(argv):
    """Convert poscar file from fractional coordinates (Direct) to Cartesian"""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=__doc__)
    # Positional arguments
    parser.add_argument('filename',
                        default=None,
                        type=str, nargs='?',
                        help='set input geometry file. If not given use stdin;')
    # Optional args
    parser.add_argument('-i',
                        action='store_true', dest='inplace',
                        help='modify file inplace;')
    parser.add_argument('--debug',
                        action='store_true', dest='debug',
                        help='show debug informations.')

    #-------------------------------------------------------------------------------
    # Initialize and check variables
    #-------------------------------------------------------------------------------
    args = parser.parse_args(argv)

    # Just to be sure, define ASE format
    ase_format = "vasp"

    # Set up LOGGER
    c_log = logging.getLogger(__name__)
    # Adopted format: level - current function name - mess. Width is fixed as visual aid
    std_format = '[%(levelname)5s - %(funcName)10s] %(message)s'
    logging.basicConfig(format=std_format)
    c_log.setLevel(logging.INFO)
    # Set debug option
    if args.debug: c_log.setLevel(logging.DEBUG)

    c_log.debug(args)

    #-------------------------------------------------------------------------------
    # Load geometry and print in cartesian
    #-------------------------------------------------------------------------------
    #++++++++ STDIN ++++++++++ If no filename, use stdin...
    if args.filename is None:
        c_log.info("Reading from stdin")
        geom = ase_sort(ase.io.read(sys.stdin, format=ase_format))
        with sys.stdout as out_stream:
            geom.write(out_stream, format=ase_format, vasp5=True, direct=False)
        # Done, exit
        return 0
    #++++++++ FILENAME ++++++++++ ...otherwise read from file
    else:
        # Check file exists
        if not os.path.exists(args.filename):
            c_log.error("File %s does not exists", args.filename)
            exit(1) # Exit with error
        geom = ase_sort(ase.io.read(args.filename, format=ase_format))

        # Modify file in place
        if args.inplace:
            geom.write(args.filename, format=ase_format, vasp5=True, direct=False)
        # Write on stdout
        else:
            with sys.stdout as out_stream:
                geom.write(out_stream, format=ase_format, vasp5=True, direct=False)
        return 0

# If executed as bash script, execute function and return exit status to bash
if __name__ == "__main__":
    exit(dir2car(sys.argv[1:]))
