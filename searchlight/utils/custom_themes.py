from rich.theme import Theme
from rich.style import Style


def danger():
    return Style(color="red", blink=True, bold=True)


def custom_theme():
    return Theme({"info": "dim cyan", "warning": "magenta", "danger": "bold red"})


def get_status_style(val):
    styles = {"green": "green", "yellow": "yellow"}
    return styles.get(val, "white on red")


def get_threshold_style(val, threshold=15):
    try:
        v = int(val)
        if v > threshold:
            return "white on red"
        if v > 0:
            return "yellow"
        return "green"
    except ValueError, TypeError:
        return "white"
