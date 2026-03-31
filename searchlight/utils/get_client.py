import typer
from client import create_os_client


def get_client(ctx: typer.Context):
    cfg = ctx.obj

    # if not cfg["auth"]:
    #     raise typer.BadParameter(
    #         "Missing --auth (or OS_AUTH env var). Format: user:password"
    #     )

    return create_os_client(
        host=cfg["host"],
        port=cfg["port"],
        auth=cfg["auth"],
        verify_certs=cfg["verify_ssl"],
        use_ssl=cfg["use_ssl"],
        ssl_show_warn=cfg["ssl_show_warn"],
    )
