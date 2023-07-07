import timeit
import logging
from math import isnan

import numpy as np
from matplotlib import pyplot as plt
from sympy.solvers import solve
from sympy import Symbol

_MAX_ITR = 10**4
_TOL_X = 1e-3
_TOL_F = 1e-3

class _NewtonLogger:

    def __init__(self, file_log_path):
        self.logger = logging.getLogger(__name__)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
            handler.close()
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(file_log_path, mode="w", encoding="utf-8")
        self.logger.addHandler(file_handler)

    def log_s_modif_head(self, step, tol_x, tol_f):
        self.logger.debug("%s-newton, tol_x = %s, tol_f = %s\n", step, tol_x, tol_f)

    def log_s_modif_itr(self, itr, x0, x1, inv_df_val, stop_cond_x, stop_cond_f):
        self.logger.debug("itr = %s:", itr)
        self.logger.debug("x%s = %s", itr, x0)
        self.logger.debug("x%s = %s", itr + 1, x1)
        self.logger.debug("||x%s - x%s||| = %s", itr + 1, itr, stop_cond_x)
        self.logger.debug("||F(x%s)|| = %s", itr + 1, stop_cond_f)
        self.logger.debug("||F'(xs)||^-1 = %s\n", inv_df_val)

    def log_time_step(self, step, result, time_ms):
        self.logger.debug("%s-newton: x = %s, itr = %s, time = %s ms",
                    step, result[0], result[1], time_ms)

def newton(f, df, x0, tol_x=_TOL_X, tol_f=_TOL_F, itr_max=_MAX_ITR, log=False, label=None):
    return s_modif(f, df, x0, 1, tol_x, tol_f, itr_max, log, label)

def modif(f, df, x0, tol_x=_TOL_X, tol_f=_TOL_F, itr_max=_MAX_ITR, log=False, label=None):
    return s_modif(f, df, x0, np.Inf, tol_x, tol_f, itr_max, log, label)

def s_modif(f, df, x0, step, tol_x=_TOL_X, tol_f=_TOL_F, itr_max=_MAX_ITR, log=False, label=None):

    newton_logger = None

    if log:
        file_log_path = f"logs/{label}_{step}_newton.log"
        newton_logger = _NewtonLogger(file_log_path)
        newton_logger.log_s_modif_head(step, tol_x, tol_f)

    if np.size(x0) > 1:
        return _array_s_modif(f, df, x0, step, tol_x, tol_f, itr_max, newton_logger)

    x0 = np.float64(x0)
    f_val = f(x0)

    for itr in range(itr_max):
        if itr % step == 0:
            inv_df_val = 1 / df(x0)
        x1 = x0 - inv_df_val * f_val
        f_val = f(x1)
        stop_cond_x = abs(x1 - x0)
        stop_cond_f = abs(f_val)
        if log:
            newton_logger.log_s_modif_itr(itr, x0, x1, inv_df_val, stop_cond_x, stop_cond_f)
        if stop_cond_x < tol_x and stop_cond_f < tol_f:
            return [x1, itr + 1]
        x0 = x1

    return [x1, itr_max]

def _array_s_modif(f, df, x0, step, tol_x, tol_f, itr_max, newton_logger):

    x0 = np.array(x0)
    f_val = np.array(f(x0))

    for itr in range(itr_max):
        if itr % step == 0:
            inv_df_val = np.linalg.inv(df(x0))
        x1 = x0 - np.dot(inv_df_val, f_val)
        f_val = np.array(f(x1))
        stop_cond_x = np.linalg.norm(x1 - x0)
        stop_cond_f = np.linalg.norm(f_val)
        if newton_logger is not None:
            newton_logger.log_s_modif_itr(itr, x0, x1, inv_df_val, stop_cond_x, stop_cond_f)
        if stop_cond_x < tol_x and stop_cond_f < tol_f:
            return [x1, itr + 1]
        x0 = x1

    return [x1, itr_max]

def measure_time_newton(f, df, x0, tol_x=_TOL_X, tol_f=_TOL_F):
    return measure_time_s_modif(f, df, x0, 1, tol_x, tol_f)

def measure_time_modif(f, df, x0, tol_x=_TOL_X, tol_f=_TOL_F):
    return measure_time_s_modif(f, df, x0, np.Inf, tol_x, tol_f)

def measure_time_s_modif(f, df, x0, step, tol_x=_TOL_X, tol_f=_TOL_F):
    time_s = timeit.repeat(repeat = 10,
                stmt = "s_modif(f, df, x0, step, tol_x, tol_f)",
                globals = {"s_modif": s_modif, "f": f, "df": df,
                           "x0": x0, "step": step,
                           "tol_x": tol_x, "tol_f": tol_f},
                number = 1)
    time_ms = np.min(time_s) * 10**3
    return time_ms

def time_step_dependency(f, df, x0, step_max, tol_x=_TOL_X, tol_f=_TOL_F, log=False, label=None):
    step_plt = []
    time_plt = []

    if log:
        file_log_path = f"logs/{label}_log_time_step.log"
        newton_logger = _NewtonLogger(file_log_path)

    for step in range(1, step_max + 1):
        result = s_modif(f, df, x0, step, tol_x, tol_f)
        if isnan(np.linalg.norm(result[0])):
            continue
        time_ms = measure_time_s_modif(f, df, x0, step)
        if log:
            newton_logger.log_time_step(step, result, time_ms)
        step_plt.append(step)
        time_plt.append(time_ms)

    time_min = np.min(time_plt)
    time_min_indices = np.where(time_plt == time_min)[0]
    step_min = [step_plt[i] for i in time_min_indices]
    print(f"time_min = {time_min} мс, step = {step_min}")

    plt.plot(step_plt, time_plt)
    plt.title(f"t(s), {label}")
    plt.xlabel("s")
    plt.ylabel("t, мс")
    plt.grid()
    plt.show()

def exact_roots(n, F_sym):
    # Find roots of equation F(x) = 0

    if n == 1:
        x_sym = Symbol("x")
    elif n > 1:
        x_sym = [Symbol(f"x[{i}]") for i in range(n)]
    else:
        raise ValueError(f"n={n} must not be less than 1")

    solutions = solve(F_sym(x_sym), x_sym, dict=True)

    for sol in solutions:
        for key in sol:
            sol[key] = sol[key].evalf()

    return solutions
