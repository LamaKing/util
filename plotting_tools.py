import numpy as np

# Shortcut to get xs and ys of list of vect.
# Useful for scatterplots.
def get_x(l):
    return np.stack(l, axis=-1)[0,:]
def get_y(l):
    return np.stack(l, axis=-1)[1,:]

# A function to plot vectors in 2D
def plot_v_2d(ax, v_origin, v_vector,
              v_color,
              v_width=0.005, nohead=False, offset=2,
              qv_opt={}):
    """Plot a collection of (origin point, vector), i.e. a vector field, on a given Matplotlib axis.

    Basically a wrapper of quiver. the ordered list of origins and vectors and we will take care of passing them.
    Plot limits will be set to a tentative value to include all the arrows.
    Aspect is set to equal so that angles are not distorted.

    If you feel you arrows should not have a direction, set nohead to True.
    """
    # Vectors with the x and y components of the origing of each vector
    oxs = get_x(v_origin)
    oys = get_y(v_origin)
    # Then 2 vectors containing all the x and y of the vect you want to plot
    xs = get_x(v_vector)
    ys = get_y(v_vector)

    # There are better ways to plot lines than killing the head of arrows. Still. Let's be lazy.
    # Set the length to 0 and the width to 1, in units of the shaft width, i.e. overlap with the body.
    if nohead: nohead={"headlength": 0, "headwidth":1}
    else: nohead = {}
    qv_opt = {**nohead, **qv_opt} # Not working as expected...

    ax.quiver(oxs, oys, xs, ys,
              color=v_color,
              scale=1, scale_units="xy", angles="xy", # Use xy as definition of angle and lenght scale. See manual.
              width=v_width,
              **qv_opt)
    offset = 2
    ax.set_xlim(min([i+j for i, j in zip(oxs,xs)]+oxs)-offset,
                max([i+j for i, j in zip(oxs,xs)])+offset) # Resize axis to accomodate all (arbitrary offset...)
    ax.set_ylim(min([i+j for i, j in zip(oys,ys)]+oys)-offset,
                max([i+j for i, j in zip(oys,ys)])+offset)
    ax.set_aspect('equal') # Square plot, do not distort angles.
    return ax # Return canvas and "axis obj", in case we want to plot over it
