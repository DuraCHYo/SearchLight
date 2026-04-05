import typer
from core.auth import create_os_client


def get_client(ctx: typer.Context):
    cfg = ctx.obj

    return create_os_client(
        host=cfg["host"],
        port=cfg["port"],
        auth=cfg["auth"],
        verify_certs=cfg["verify_ssl"],
        use_ssl=cfg["use_ssl"],
        ssl_show_warn=cfg["ssl_show_warn"],
    )
