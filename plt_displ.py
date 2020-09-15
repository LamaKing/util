#!/usr/bin/env python3

import sys
import os, argparse, logging
import ase.io
from ase.build import sort as ase_sort
from ase.io import read as ase_read
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

o = np.array([0,0,0])

def plot_displ(ax, start, end,
               atm_scale=1, v_len=1, normalize=False, plt_uc=False, plt_endpt=False):
    """sa sa check"""
    if False in [isinstance(start, ase.Atoms), isinstance(end, ase.Atoms)]:
        raise TypeError("Start and end geometry need to be ASE Atoms obj")

    p0 = start.positions
    p1 = end.positions
    dp = p1 - p0

    # Get color and atom size from mendeleev pkg (easier than write the dictionary myself)
    from mendeleev import element
    elem_color = [element(a.symbol).jmol_color for a in start]
    elem_size = np.array([element(a.symbol).covalent_radius for a in start])

    if plt_uc:
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        a,b,c = start.get_cell()

        # Tested only for hexagonal cell
        verts = np.stack([o, a, a+b, b, o, # Base
                          c+o, # Move to top
                          c+o+a, o+a, c+o+a, # Move to top a, go down to base a and back up
                          c+o+a+b, o+a+b, c+o+a+b, # Same for second vertex in base
                          c+o+b, o+b, c+o+b,
                          c+o, o]) # Return to origin
        x = verts[:, 0]
        y = verts[:, 1]
        z = verts[:, 2]
        uc_style = {'alpha': 0., # Controls only the alpha of the faces, apparently
                    'facecolors': None,
                    'edgecolors' : "black",
                    'ls': "--",
                    'lw': 0.4}

        verts = [list(zip(x,y,z))]
        uc = Poly3DCollection(verts, **uc_style)
        ax.add_collection3d(uc)


    # Plot the displacement arrows
    ax.quiver(p0[:, 0], p0[:, 1], p0[:, 2],
              dp[:, 0], dp[:, 1], dp[:, 2],
              length=v_len, normalize=normalize)

    # Plot the atoms in intial position
    ax.scatter(p0[:, 0], p0[:, 1], p0[:, 2],
               c=elem_color,
               edgecolors="black",
               s=atm_scale*elem_size)

    if plt_endpt:
        end_scale = 0.1
        p1_plot = (p0+v_len*dp) # Compute the scaled position of the end atom
        ax.scatter(p1_plot[:, 0], p1_plot[:, 1], p1_plot[:, 2],
                   c=elem_color,
                   edgecolors="gray",
                   s=atm_scale*elem_size*end_scale)

        # Plot ending point unit cell
        if plt_uc:
            from mpl_toolkits.mplot3d.art3d import Poly3DCollection
            a,b,c = end.get_cell()

            # Tested only for hexagonal cell
            verts = np.stack([o, a, a+b, b, o, # Base
                              c+o, # Move to top
                              c+o+a, o+a, c+o+a, # Move to top a, go down to base a and back up
                              c+o+a+b, o+a+b, c+o+a+b, # Same for second vertex in base
                              c+o+b, o+b, c+o+b,
                              c+o, o]) # Return to origin
            x = verts[:, 0]
            y = verts[:, 1]
            z = verts[:, 2]
            uc_style = {'alpha': 0., # Controls only the alpha of the faces, apparently
                        'facecolors': None,
                        'edgecolors' : "gray",
                        'ls': "--",
                        'lw': 0.2}

            verts = [list(zip(x,y,z))]
            uc = Poly3DCollection(verts, **uc_style)
            ax.add_collection3d(uc)

    return ax

def plot_displ_CLI(argv):
    """sa sa check"""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=plot_displ_CLI.__doc__)
    # Positional arguments
    # Optional args
    parser.add_argument('-s', '--start',
                        dest='start', default="POSCAR",
                        help='starting geometry (def: POSCAR);')
    parser.add_argument('-e', '--end',
                        dest='end', default="CONTCAR",
                        help='ending geometry (def: CONTCAR);')
    parser.add_argument('-l', '--len',
                        dest='v_len', type=float, default=1.0,
                        help='scaling factor for displacement vectors visualization (def: 1);')
    parser.add_argument('--size',
                        dest='atm_scale', type=float, default=1.0,
                        help='scaling factor for atom size (def: 1);')
    parser.add_argument('--end_pt',
                        action='store_true', dest='show_endpt',
                        help='show minimization endpoint')
    parser.add_argument('--no_norm',
                        action='store_true', dest='norm',
                        help='normalize vectors to same size.')
    parser.add_argument('--rep',
                        dest='replica', type=int, nargs=3, default=(1,1,1),
                        help='replicate systems along unit cell.')
    parser.add_argument('--uc',
                        dest='unitcell', action='store_true',
                        help='plot unit cell.')
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
    # Load geometry
    #-------------------------------------------------------------------------------

    start = ase_read(args.start)
    del start.constraints
    try:
        start = ase_sort(start*args.replica)
    except Exception as e:
        c_log.error("Starting geom replication went wrong. Expect errors")

    end = ase_read(args.end)
    del end.constraints
    try:
        end = ase_sort(end*args.replica)
    except Exception as e:
        c_log.error("Ending geom replication went wrong. Expect errors")

    #-------------------------------------------------------------------------------
    # Plot
    #-------------------------------------------------------------------------------
    fig = plt.figure()
    fig.set_dpi(150)
    ax = fig.gca(projection='3d')

    ax = plot_displ(ax, start, end,
                    atm_scale=args.atm_scale, # size of atoms
                    v_len=args.v_len, normalize=args.norm, # displacement arrows
                    plt_uc=args.unitcell, plt_endpt=args.show_endpt) # To plot or not to plot
    plt.show()

if __name__ == "__main__":
    plot_displ_CLI(sys.argv[1:])
