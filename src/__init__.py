import os

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def setup_plot():
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
