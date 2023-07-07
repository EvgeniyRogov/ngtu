from scipy.integrate import solve_ivp

_MAX_ITR = 100
_TOL_S = 1e-3
_TOL_M = 1e-3

def shooting_bvp(odes, t_eval, t_span, x_init, s0, tol_s=_TOL_S, tol_m=_TOL_M, max_itr=_MAX_ITR):

    A, B = x_init

    sol_ivp = solve_ivp(odes, t_span=t_span, y0=[A, s0, 0, 1], t_eval=t_eval)
    x = sol_ivp.y[0]
    xb = x[-1]
    m = xb - B
    zb = sol_ivp.y[2][-1]

    for itr in range(max_itr):
        s1 = s0 - m / zb
        sol_ivp = solve_ivp(odes, t_span=t_span, y0=[A, s1, 0, 1], t_eval=t_eval)
        x = sol_ivp.y[0]
        xb = x[-1]
        m = xb - B
        zb = sol_ivp.y[2][-1]
        if abs(s1 - s0) < tol_s and abs(m) < tol_m:
            return [x, s1, itr + 1]
        s0 = s1

    return [x, s1, max_itr]
