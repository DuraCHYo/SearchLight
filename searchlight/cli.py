import typer
from typing import Optional
import json
import urllib3
from services.security import SecurityService
from services.index_management import PoliciesService
from services.tasks import TasksService
from services.nodes import NodeService
from utils.get_client import get_client
from utils.logger import handle_errors
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()
security_app = typer.Typer(help="Control security")
policies_app = typer.Typer(help="Control policies")
tasks_app = typer.Typer(help="Control cluster tasks")
nodes_app = typer.Typer(help="Control cluster nodes")


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
def security_list_roles(ctx: typer.Context):
    """List all roles

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    roles = services.get_roles()
    typer.echo(json.dumps(roles, indent=2))


@security_app.command("list-users")
@handle_errors
def security_list_users(ctx: typer.Context):
    """List users

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    users = services.get_users()

    table = Table(title="OpenSearch Users")
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Backend Roles", style="magenta")
    table.add_column("Reserved", style="green")

    for name, info in users.items():
        roles = ", ".join(info.get("backend_roles", []))
        reserved = "Yes" if info.get("reserved") else "No"
        table.add_row(name, roles, reserved)

    console.print(table)


@security_app.command("health")
@handle_errors
def security_plugin_health(ctx: typer.Context):
    """Security plugin health

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    health = services.get_health()
    typer.secho(json.dumps(health, indent=2))


@security_app.command("whoami")
@handle_errors
def security_who_am_i(ctx: typer.Context):
    """Gets the identity information for the user currently logged in.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    who_am_i = services.who_am_i()
    typer.secho(json.dumps(who_am_i, indent=2))


@policies_app.command("list-policies")
@handle_errors
def policies_list_policies(
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
    typer.echo(json.dumps(policies, indent=2))


@policies_app.command("ensure")
@handle_errors
def policies_ensure_policy(
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
    _, created = services.ensure_policy_exists(policy_name=policy_id, body=body)

    if created:
        typer.secho(f"Policy '{policy_id}' already created", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"Policy '{policy_id}' already exists. No action required",
            fg=typer.colors.BLUE,
        )


@tasks_app.command("get-task-info")
@handle_errors
def tasks_get_task_info(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID"),
):
    """Get information about task

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = TasksService(client, task_id)
    data = services.get_task_info(task_id)
    typer.secho(json.dumps(data, indent=2))


@tasks_app.command("cancel-task")
@handle_errors
def tasks_cancel_task(
    ctx: typer.Context,
    task_id: str = typer.Argument(None, help="Task ID"),
):
    """Cancel task by ID

    Args:
        ctx (typer.Context): _description_
        task_id (str, optional): _description_. Defaults to typer.Argument(None, help="Task ID").
    """
    client = get_client(ctx)
    services = TasksService(client, task_id)
    data = services.cancel_task(task_id)
    typer.secho(json.dumps(data, indent=2))


@tasks_app.command("list-tasks")
@handle_errors
def tasks_get_tasks_list(ctx: typer.Context):
    """List tasks

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = TasksService(client)
    data = services.get_tasks_list()

    table = Table(title="Running Tasks")
    table.add_column("Node Name", style="cyan", no_wrap=True)
    table.add_column("Node IP", style="dim")
    table.add_column("Task ID", style="yellow")
    table.add_column("Action", style="red")
    table.add_column("Running Time (ms)", style="green")

    nodes = data.get("nodes", {})
    for _, node_info in nodes.items():
        node_name = node_info.get("name", "Unknown")
        node_ip = node_info.get("ip", "N/A")
        tasks = node_info.get("tasks", {})

        if not tasks:
            continue

        for _, task_info in tasks.items():
            task_id_short = str(task_info.get("id"))
            action = task_info.get("action", "N/A")
            duration_ms = f"{task_info.get('running_time_in_nanos', 0) / 1_000_000:.3f}"

            parent = task_info.get("parent_task_id", "-")
            prefix = "┗━ " if parent != "-" else ""

            table.add_row(
                node_name,
                node_ip,
                f"{prefix}{task_id_short}",
                action,
                duration_ms,
            )

    console = Console()
    console.print(table)


@nodes_app.command("get-hot-thread")
@handle_errors
def nodes_get_hot_threads(
    ctx: typer.Context,
    node_id: Optional[str] = typer.Argument(None, help="Node ID"),
):
    """Get hot threads

    Args:
        ctx (typer.Context): _description_
        node_id (Optional[str], optional): _description_. Defaults to typer.Argument(None, help="Node ID").
    """
    client = get_client(ctx)
    services = NodeService(client, node_id=node_id)
    filtered_lines = []
    found_start = False
    if node_id:
        data = services.get_hot_threads()
    else:
        data = services.get_hot_threads()
    for line in data.splitlines():
        clean_line = line.strip()

        if "Hot threads" in clean_line:
            found_start = True

        if found_start:
            filtered_lines.append(line)

    result = "\n".join(filtered_lines)
    typer.secho(result.strip(), fg=typer.colors.RED)


@nodes_app.command("node-info")
@handle_errors
def nodes_get_node_info(
    ctx: typer.Context,
    node_id: Optional[str] = typer.Argument(None, help="Node ID"),
    metric: Optional[str] = typer.Option(
        "_all",
        "--metric",
        "-m",
        help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list",
    ),
):
    """Get node info

    Args:
        ctx (typer.Context): _description_
        node_id (Optional[str], optional): _description_. Defaults to typer.Argument(None, help="Node ID").
        metric (Optional[str], optional): _description_. Defaults to typer.Option( "_all", "--metric", "-m", help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list", ).
    """
    client = get_client(ctx)
    services = NodeService(client, node_id=node_id, metric=metric)

    data = services.get_node_info()

    typer.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    app()
