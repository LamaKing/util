#!/usr/bin/env python3

import sys
import os, argparse, logging
from pymatgen.io.vasp import Vasprun
from pymatgen.io.ase import AseAtomsAdaptor

def get_ion_geoms(argv):
    """"""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=__doc__)
    # Positional arguments
    parser.add_argument('filename',
                        default="vasprun.xml",
                        type=str, nargs='?',
                        help='set input xml file. Default vasprun.xml;')
    # Optional args
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

    # Quickly load the xml, skip big parts to go faster
    vasprun= Vasprun(args.filename,
                     parse_projected_eigen=False,
                     parse_eigen=False,
                     parse_dos=False,
                     exception_on_bad_xml=False,
                     parse_potcar_file=False)

    #  Conver between PyMatGen Strcutre and ASE
    #  Just because we are more familiar with the latter
    ase_bridge=AseAtomsAdaptor()

    #  For each structure, save a POSCAR with the ion step in front (easier to read in right order from bash)
    for i, structure in enumerate(vasprun.structures):
        ase_bridge.get_atoms(structure).write("%i-ion_step.vasp" % i,
                                              vasp5=True)
    return Vasprun.structures

# If executed as bash script, execute function and return exit status to bash
if __name__ == "__main__":
    get_ion_geoms(sys.argv[1:])
