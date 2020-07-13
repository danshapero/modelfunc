import firedrake
import icepack
from icepack.constants import weertman_sliding_law as m


def viscosity(u, h, grounded, floating, A, theta):
    """Combine existing A on grounded ice with theta^2 from floating ice.
    Parameters
    ----------
    u : firedrake function
        modelled velocity
    h : firedrake function
        model thickness
    grounded : firedrake function
        Mask with 1s for grounded 0 for floating.
    floating : firedrake function
        Mask with 1s for floating 0 for grounded.
    A : firedrake function
        A for grounded areas
    theta : firedrake function
        theta for A on floating ice as theta^2
    Returns
    -------
    viscosityFunction function
        Viscosity funciton for model
    """
    # A = grounded * A + floating * theta**2
    A = grounded * A + floating * firedrake.exp(theta)
    return icepack.models.viscosity.viscosity_depth_averaged(u, h, A)


def weertmanFriction(u, grounded, beta, uThresh):
    """Friction coefficient for weertman sliding law
    Parameters
    ----------
    u : firedrake function
        modelled velocity
    grounded : firedrake function
        Mask with 1s for grounded 0 for floating.
    beta : firedrake function
        Beta for friction model with C=beta^2

    Returns
    -------
    frictionFunction function
        Bed friction model
    """
    C = grounded * beta**2
    return icepack.models.friction.bed_friction(u=u, C=C)


# Note m is a global variable
def schoofFriction(u, grounded, beta, uThresh):
    """Friction coefficient for regularized coloumb (Schoof) sliding law
    Parameters
    ----------
    u : firedrake function
        modelled velocity
    grounded : firedrake function
        Mask with 1s for grounded 0 for floating.
    beta : firedrake function
        Beta for friction model with C=beta^2
    uThresh : float
        Velocity transition for sliding law
    Returns
    -------
    frictionFunction function
        Bed friction model
    """
    C = grounded * beta**2
    mExp = (1/m + 1)
    U = firedrake.sqrt(firedrake.inner(u, u))
    return C * (uThresh**mExp + U**mExp)**(m/(m+1))
