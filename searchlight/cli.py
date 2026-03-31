import typer
import json
import urllib3
from services.security import SecurityService
from services.policies import PoliciesService
from utils.get_client import get_client
from utils.logger import handle_errors

app = typer.Typer()
security_app = typer.Typer(help="Control security")
policies_app = typer.Typer(help="Control policies")


@app.callback()
@handle_errors
def main(
    ctx: typer.Context,
    host: str = typer.Option("localhost", envvar="OS_HOST"),
    port: int = typer.Option(9200, envvar="OS_PORT"),
    auth: str = typer.Option(None, envvar="OS_AUTH"),
    verify_ssl: bool = typer.Option(True, "--verify-ssl/--disable-verify-ssl"),
    use_ssl: bool = typer.Option(True, "--use-ssl/--disable-use-ssl"),
    ssl_show_warn: bool = typer.Option(True, "--show-warn/--disable-warn"),
):
    if not ssl_show_warn:
        urllib3.disable_warnings()

    ctx.obj = {
        "host": host,
        "port": port,
        "auth": auth,
        "verify_ssl": verify_ssl,
        "use_ssl": use_ssl,
        "ssl_show_warn": ssl_show_warn,
    }


@security_app.command("list-roles")
@handle_errors
def list_roles(ctx: typer.Context):
    """List all roles

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    providers = SecurityService(client)
    roles = providers.get_roles()
    typer.echo(json.dumps(roles, indent=4))


@security_app.command("list-users")
@handle_errors
def list_users(ctx: typer.Context):
    """List all users

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    providers = SecurityService(client)
    users = providers.get_users()
    typer.echo(json.dumps(users, indent=4))


@policies_app.command("list-policies")
@handle_errors
def list_policies(
    ctx: typer.Context,
    policy_id: str = typer.Argument(None, help="Policy name (optional)"),
):
    """List all index policies

    Args:
        ctx (typer.Context): _description_
        policy_id (str, optional): _description_. Defaults to typer.Argument(None, help="Policy name (optional)").
    """
    client = get_client(ctx)
    services = PoliciesService(client)
    policies = services.get_policy(policy_name=policy_id)
    typer.echo(json.dumps(policies, indent=4))


@policies_app.command("ensure")
@handle_errors
def ensure_policy(
    ctx: typer.Context,
    policy_id: str = typer.Argument(..., help="Policy ID"),
    file: typer.FileText = typer.Option(
        ..., "--file", "-f", help="Path to JSON-policy file"
    ),
):
    """Checks if policy already exists

    Args:
        ctx (typer.Context): _description_
        policy_id (str, optional): _description_. Defaults to typer.Argument(..., help="Policy ID").
        file (typer.FileText, optional): _description_. Defaults to typer.Option( ..., "--file", "-f", help="Path to JSON-policy file" ).
    """
    client = get_client(ctx)
    services = PoliciesService(client)

    body = json.load(file)
    result, created = services.ensure_policy_exists(policy_name=policy_id, body=body)

    if created:
        typer.secho(f"Policy '{policy_id}' already created", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"Policy '{policy_id}' already exists. No action required",
            fg=typer.colors.BLUE,
        )


if __name__ == "__main__":
    app()
