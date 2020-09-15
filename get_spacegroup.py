#!/usr/bin/env python3

import sys
import os, argparse, logging
from ase.io import read
from ase.spacegroup import get_spacegroup

def get_spgroup(argv):
    """Get spacegroup from list of files"""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=__doc__)
    # Optional args
    parser.add_argument('-f', '--files',
                        dest="filenames", default=["POSCAR", "CONTCAR"],
                        type=str, nargs='+',
                        help='geometry files. Default POSCAR, CONTCAR;')
    parser.add_argument('--symprec',
                        dest='symprec', type=float, default=1e-5,
                        help='set precision on symmetry operations.')
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

    #-------------------------------------------------------------------------------
    # Load geometry and print in cartesian
    #-------------------------------------------------------------------------------

    spgroups = [get_spacegroup(read(filename), symprec=args.symprec) for filename in args.filenames]

    for f, spg in zip(args.filenames, spgroups):
        print("Geom %s Spacegroup symbol %s (%i)" % (f, spg.symbol, spg.no))

    return spgroups

# If executed as bash script, execute function and return exit status to bash
if __name__ == "__main__":
    get_spgroup(sys.argv[1:])
