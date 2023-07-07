import numpy as np

_MAX_ITR = 10**6
_H = 1e-3
_TOL = 1e-3

def _alpha(t, a0):
    return t**(-a0)

def _gamma(t, g0):
    return t**(-g0)

def _delta(t, b0):
    return t**(-b0)

def _f(t, f0, b0):
    # return f0 + _delta(t, b0)
    return f0*(1 + _delta(t, b0))

def _df(t, f0, b0):
    # return -b0 / t**(b0 + 1)
    return -f0 * b0 / t**(b0 + 1)

def _F_cont(n, t, x, A, dA, f0, g0):
    if n == 1:
        return -_gamma(t, g0) * dA(x)**(-1) * (A(x) - f0)
    elif n > 1:
        return -_gamma(t, g0) * np.dot(np.linalg.inv(dA(x)), A(x) - f0)
    else:
        raise ValueError(f"n={n} must not be less than 1")

def _F_pertubed_right(n, t, x, A, dA, f0, params):

    b0, a0, g0 = params

    if n == 1:
        return -(dA(x) + _alpha(t, a0))**-1 * (_gamma(t, g0) *
            (A(x) + _alpha(t, a0) * x - _f(t, f0, b0)) + _df(t, f0, b0))
    if n > 1:
        return np.dot(-np.linalg.inv(dA(x) + _alpha(t, a0) * np.eye(n)),
            _gamma(t, g0) * (A(x) + _alpha(t, a0) * x - _f(t, f0, b0)) + _df(t, f0, b0))
    else:
        raise ValueError(f"n={n} must not be less than 1")

def _F_pertubed_operator(n, t, x, A, dA, f0, params):

    b0, a0, g0, h0 = params

    if n == 1:
        return -(dA(t, x, h0) + _alpha(t, a0))**-1 * (_gamma(t, g0) *
            (A(t, x, h0) + _alpha(t, a0) * x - _f(t, f0, b0)) + _df(t, f0, b0))
    if n > 1:
        return np.dot(-np.linalg.inv(dA(t, x, h0) + _alpha(t, a0) * np.eye(n)),
            _gamma(t, g0) * (A(t, x, h0) + _alpha(t, a0) * x - _f(t, f0, b0)) + _df(t, f0, b0))
    else:
        raise ValueError(f"n={n} must not be less than 1")

def solve_cont(A, dA, f0, t0, x0, g0, dt=_H, tol=_TOL, log=False, coords=None):
    return _solve_init_problem(A, dA, f0, t0, x0, g0, dt, tol, log, coords, F=_F_cont)

def solve_pertubed_right(A, dA, f0, t0, x0, params, dt=_H, tol=_TOL, log=False, coords=None):
    # Use params = (b0, a0, g0)
    return _solve_init_problem(A, dA, f0, t0, x0, params, dt, tol, log, coords, F=_F_pertubed_right)

def solve_pertubed_operator(A, dA, f0, t0, x0, params, dt=_H, tol=_TOL, log=False, coords=None):
    # Use params = (b0, a0, g0, h0)
    return _solve_init_problem(A, dA, f0, t0, x0, params, dt, tol, log, coords, F=_F_pertubed_operator)

def _solve_init_problem(A, dA, f0, t0, x0, params, dt, tol, log, coords, F):

    x0 = np.array(x0)
    f0 = np.array(f0)
    n = np.size(x0)

    itr = 1
    t = t0
    x = x0

    while itr < _MAX_ITR:
        k1 = dt * F(n, t, x, A, dA, f0, params)
        k2 = dt * F(n, t + dt / 2, x + k1 / 2, A, dA, f0, params)
        k3 = dt * F(n, t + dt / 2, x + k2 / 2, A, dA, f0, params)
        k4 = dt * F(n, t + dt, x + k3, A, dA, f0, params)
        x = x + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t = t + dt

        if coords is not None:
            coords[0].append(t)
            for i in range(1, n + 1):
                coords[i].append(x)

        if np.linalg.norm(A(x) - f0) < tol:
            return [x, t, itr]

        if log:
            print(f"x = {x}, t = {t}, itr = {itr}")

        itr = itr + 1

    return [x, t, _MAX_ITR]
