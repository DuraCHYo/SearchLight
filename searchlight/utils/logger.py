from functools import wraps
from typer import secho, Exit


def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            secho(f"Fatal error: {e}", fg="red", bold=True, err=True)
            raise Exit(1)

    return wrapper
