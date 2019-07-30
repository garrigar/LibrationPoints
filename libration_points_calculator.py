from enum import Enum
from typing import Callable
from collections import namedtuple
import time

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# from scipy.interpolate import interp1d

import tkinter
from tkinter import ttk


class TimeProfiler:

    def __init__(self, enabled: bool = True, label: str = 'TimeProfiler'):
        self._enabled = enabled
        self._label = label

    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._enabled:
            print("{}: Elapsed time: {:.3f} sec".format(self._label, (time.time() - self._startTime)))


class CalcTypes(Enum):
    NEWTON = "Newton's"
    DICHOTOMY = "Dichotomy"


Constants = namedtuple('Constants', [
    'MIN_CALC_POINTS_COUNT',
    'MAX_CALC_POINTS_COUNT',
    'DEFAULT_CALC_POINTS_COUNT',
    'EPSILONS'
])
constants = Constants(2, 100000, 10000, {'10^({})'.format(i): 10 ** i for i in range(-1, -11, -1)})


class Launcher(tkinter.Tk):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title('Libration Points Calculator launcher')
        self.geometry('370x200')
        self.minsize(370, 200)

        calc_types = {a.value: a for a in CalcTypes}
        calc_points_range = range(constants.MIN_CALC_POINTS_COUNT, constants.MAX_CALC_POINTS_COUNT + 1)

        frame = ttk.Frame(self)
        frame.pack(expand=1)

        label1 = ttk.Label(frame, text='Calculation method:')
        label1.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.W)
        combobox_method = ttk.Combobox(frame, state='readonly', values=list(calc_types.keys()))
        combobox_method.current(0)
        combobox_method.grid(row=0, column=1, padx=5, pady=5, sticky=tkinter.W)

        label2 = ttk.Label(frame, text='Number of points ({:d}-{:d}):'.format(
            constants.MIN_CALC_POINTS_COUNT, constants.MAX_CALC_POINTS_COUNT
        ))
        label2.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.W)
        points_count_var = tkinter.StringVar()
        points_count_var.set(str(constants.DEFAULT_CALC_POINTS_COUNT))
        spinbox = ttk.Spinbox(frame, values=tuple(calc_points_range), textvariable=points_count_var)
        spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tkinter.W)

        label3 = ttk.Label(frame, text='Wanted accuracy:')
        label3.grid(row=2, column=0, padx=5, pady=5, sticky=tkinter.W)
        combobox_eps = ttk.Combobox(frame, state='readonly', values=list(constants.EPSILONS.keys()))
        combobox_eps.current(6)
        combobox_eps.grid(row=2, column=1, padx=5, pady=5, sticky=tkinter.W)

        chk_time = tkinter.BooleanVar()
        chk_time.set(False)
        checkbutton_time = ttk.Checkbutton(frame, text='Enable time logging', variable=chk_time)
        checkbutton_time.grid(row=3, column=1, padx=5, pady=5, sticky=tkinter.W)

        chk_extended = tkinter.BooleanVar()
        chk_extended.set(True)
        checkbutton_ext = ttk.Checkbutton(frame, text='Draw extended graphs', variable=chk_extended)
        checkbutton_ext.grid(row=4, column=1, padx=5, pady=5, sticky=tkinter.W)

        def handle_button_click():
            try:
                i = int(points_count_var.get())
                if i in calc_points_range:
                    calculate_and_show(calc_types.get(combobox_method.get()), i,
                                       constants.EPSILONS.get(combobox_eps.get()), chk_time.get(), chk_extended.get())
                else:
                    points_count_var.set(str(constants.DEFAULT_CALC_POINTS_COUNT))
            except ValueError:
                points_count_var.set(str(constants.DEFAULT_CALC_POINTS_COUNT))

        button = ttk.Button(frame, text='Start', command=handle_button_click)
        button.grid(row=5, column=1, padx=5, pady=5, sticky=tkinter.E)


class ResultWindow(tkinter.Tk):

    def __init__(self, calc_type: CalcTypes, eps: float, data: list, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title(
            'Result of calculations: {} method, {:d} points, eps = {}'.format(calc_type.value, len(data[0]),
                                                                              next(eps_str
                                                                                   for eps_str, eps_val
                                                                                   in constants.EPSILONS.items()
                                                                                   if eps_val == eps)
                                                                              )
        )
        self.geometry('1525x600')
        self.minsize(1525, 600)

        list_x1 = list(data[0].keys())
        list_y1 = list(data[0].values())
        list_x2 = list(data[1].keys())
        list_y2 = list(data[1].values())
        list_x3 = list(data[2].keys())
        list_y3 = list(data[2].values())

        # self._f1 = interp1d(list_x1, list_y1)
        # self._f2 = interp1d(list_x2, list_y2)
        # self._f3 = interp1d(list_x3, list_y3)

        graphs_frame = ttk.LabelFrame(self, text='Graphs')
        graphs_frame.pack(expand=1)
        graph1_frame = self._build_graph_frame(graphs_frame, 'L1', list_x1, list_y1)
        graph1_frame.pack(side=tkinter.LEFT)
        graph2_frame = self._build_graph_frame(graphs_frame, 'L2', list_x2, list_y2)
        graph2_frame.pack(side=tkinter.LEFT)
        graph3_frame = self._build_graph_frame(graphs_frame, 'L3', list_x3, list_y3)
        graph3_frame.pack(side=tkinter.LEFT)

    @staticmethod
    def _build_graph_frame(master, label_text, list_x, list_y):
        frame = ttk.LabelFrame(master, text=label_text)

        fig = Figure(figsize=(5, 5), dpi=100)
        fig.suptitle(label_text)
        axes = fig.add_subplot(111)
        axes.plot(list_x, list_y)
        axes.grid()
        axes.set_xlabel('α')
        axes.set_ylabel('y', rotation=0)

        graph = FigureCanvasTkAgg(fig, master=frame)
        # graph.draw()
        graph.get_tk_widget().pack(fill=tkinter.BOTH)

        toolbar = NavigationToolbar2Tk(graph, frame)
        # toolbar.update()
        toolbar.pack(fill=tkinter.BOTH)

        return frame


def calculate_and_show(calc_type: CalcTypes,
                       points_count: int = constants.DEFAULT_CALC_POINTS_COUNT, eps: float = 1e-7,
                       time_logging: bool = False, extended_graphs: bool = False):
    ResultWindow(calc_type, eps, calculate_data_dicts(calc_type, points_count, eps, time_logging,
                                                      extended_graphs)).mainloop()


def calculate_data_dicts(calc_type: CalcTypes,
                         points_count: int = constants.DEFAULT_CALC_POINTS_COUNT, eps: float = 1e-7,
                         time_logging: bool = False, extended_graphs: bool = False):
    if points_count not in range(constants.MIN_CALC_POINTS_COUNT, constants.MAX_CALC_POINTS_COUNT + 1):
        print('calculate_data_dicts: Points count out of allowed range (must be from {:d} to {:d})'.format(
            constants.MIN_CALC_POINTS_COUNT, constants.MAX_CALC_POINTS_COUNT
        ))
        print('Using default value for points count ({:d})'.format(constants.DEFAULT_CALC_POINTS_COUNT))
        points_count = constants.DEFAULT_CALC_POINTS_COUNT

    answer = []

    left_border = 0.0
    if extended_graphs:
        right_border = 1.0
    else:
        right_border = 0.5
    delta = (right_border - left_border) / (points_count - 1)

    # ----------------------------L1------------------------------

    def f1(y: float, alpha: float) -> float:
        return y - (alpha / (((1 - alpha) + y) ** 2)) + ((1 - alpha) / ((alpha - y) ** 2))

    def f1_p(y: float, alpha: float) -> float:
        return 1 + ((2 * (1 - alpha)) / ((alpha - y) ** 3)) + ((2 * alpha) / (((1 - alpha) + y) ** 3))

    ans1 = {left_border: -1}
    a = left_border
    y_last = -1
    if calc_type == CalcTypes.NEWTON:
        with TimeProfiler(time_logging, 'Calculating L1 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_newton(f1, f1_p, y_last, a, eps)
                ans1[a] = y_last

            if extended_graphs:
                ans1[right_border] = 1
            else:
                ans1[right_border] = find_root_newton(f1, f1_p, y_last, right_border, eps)  # 0

    elif calc_type == CalcTypes.DICHOTOMY:
        with TimeProfiler(time_logging, 'Calculating L1 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_dichotomy(f1, -1, 1, a, eps)
                ans1[a] = y_last

            if extended_graphs:
                ans1[right_border] = 1
            else:
                ans1[right_border] = 0  # find_root_dichotomy(f1, -1, 1, right_border, eps)

    answer.append(ans1)

    # ----------------------------L2------------------------------

    def f2(y: float, alpha: float) -> float:
        return y + (alpha / (((1 - alpha) + y) ** 2)) + ((1 - alpha) / ((alpha - y) ** 2))

    def f2_p(y: float, alpha: float) -> float:
        return 1 + ((2 * (1 - alpha)) / ((alpha - y) ** 3)) - ((2 * alpha) / (((1 - alpha) + y) ** 3))

    ans2 = {left_border: -1}
    a = left_border
    y_last = -1
    if calc_type == CalcTypes.NEWTON:
        with TimeProfiler(time_logging, 'Calculating L2 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_newton(f2, f2_p, y_last, a, eps)
                ans2[a] = y_last

            ans2[right_border] = find_root_newton(f2, f2_p, y_last, right_border, eps)

    elif calc_type == CalcTypes.DICHOTOMY:
        with TimeProfiler(time_logging, 'Calculating L2 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_dichotomy(f2, -1.5, -1, a, eps)
                ans2[a] = y_last

            ans2[right_border] = find_root_dichotomy(f2, -1.5, -1, right_border, eps)

    answer.append(ans2)

    # ----------------------------L3------------------------------

    def f3(y: float, alpha: float) -> float:
        return y - (alpha / (((1 - alpha) + y) ** 2)) - ((1 - alpha) / ((alpha - y) ** 2))

    def f3_p(y: float, alpha: float) -> float:
        return 1 - ((2 * (1 - alpha)) / ((alpha - y) ** 3)) + ((2 * alpha) / (((1 - alpha) + y) ** 3))

    ans3 = {left_border: 1}
    a = left_border
    y_last = 1
    if calc_type == CalcTypes.NEWTON:
        with TimeProfiler(time_logging, 'Calculating L3 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_newton(f3, f3_p, y_last, a, eps)
                ans3[a] = y_last

            if extended_graphs:
                ans3[right_border] = 1
            else:
                ans3[right_border] = find_root_newton(f3, f3_p, y_last, right_border, eps)

    elif calc_type == CalcTypes.DICHOTOMY:
        with TimeProfiler(time_logging, 'Calculating L3 location by {} method ({:d} points, eps = {:g})'.format(
                calc_type.value, points_count, eps)):
            for i in range(points_count - 2):
                a += delta
                y_last = find_root_dichotomy(f3, 1, 1.5, a, eps)
                ans3[a] = y_last

            if extended_graphs:
                ans3[right_border] = 1
            else:
                ans3[right_border] = find_root_dichotomy(f3, 1, 1.5, right_border, eps)

    answer.append(ans3)

    # ------------------------------------------------------------

    return answer


def find_root_dichotomy(f: Callable[[float, float], float], xn: float, xk: float,
                        param_a: float, epsy: float = 1e-7) -> float:
    xi = None
    if f(xn, param_a) == 0:
        return xn
    if f(xk, param_a) == 0:
        return xk
    while xk - xn > epsy:
        dx = (xk - xn) / 2
        xi = xn + dx
        if f(xn, param_a) * f(xi, param_a) < 0:
            xk = xi
        else:
            xn = xi
    return xi


def find_root_newton(f: Callable[[float, float], float], f_prime: Callable[[float, float], float], x0: float,
                     param_a: float, eps: float = 1e-7, kmax: int = 1e3) -> float:
    """
    solves f(x) = 0 by Newton's method with precision eps
    :param param_a: parameter a
    :param kmax: max iterations count
    :param f: f
    :param f_prime: f'
    :param x0: starting point
    :param eps: precision wanted
    :return: root of f(x) = 0
    """
    x, x_prev, i = x0, x0 + 2 * eps, 0

    while abs(x - x_prev) >= eps and i < kmax:
        x, x_prev, i = x - f(x, param_a) / f_prime(x, param_a), x, i + 1

    return x


def launch():
    Launcher().mainloop()


if __name__ == "__main__":
    launch()
