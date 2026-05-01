from typing import Annotated, Optional

import typer
import urllib3
from rich import print_json
from rich.console import Console
from rich.table import Table
from services.cat import CatService  # ty:ignore[unresolved-import]
from services.ism_policies import PoliciesService  # ty:ignore[unresolved-import]
from services.nodes import NodeService  # ty:ignore[unresolved-import]
from services.security import SecurityService  # ty:ignore[unresolved-import]
from services.tasks import TasksService  # ty:ignore[unresolved-import]
from utils.custom_themes import (  # ty:ignore[unresolved-import]
    get_status_style,
    get_threshold_style,
)
from utils.get_client import get_client  # ty:ignore[unresolved-import]
from utils.logger import handle_errors  # ty:ignore[unresolved-import]

console = Console(color_system="auto", force_terminal=True)
app = typer.Typer()
user_friendly_cat_app = typer.Typer(help="User Friendly CAT APIs")
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
    if ctx.resilient_parsing:
        return
    ctx.obj = {
        "host": host,
        "port": port,
        "auth": auth,
        "verify_ssl": verify_ssl,
        "use_ssl": use_ssl,
        "ssl_show_warn": ssl_show_warn,
    }


def get_console(ctx: typer.Context) -> Console:
    return ctx.obj["console"]


@security_app.command("list-roles")
@handle_errors
def security_list_roles(ctx: typer.Context):
    """List all roles

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    data = services.get_roles()
    print_json(data=data)


@security_app.command("list-users")
@handle_errors
def security_list_users(ctx: typer.Context):
    """List users

    Args:
        ctx (typer.Context): _description_
    """
    console = get_console(ctx)
    client = get_client(ctx)
    services = SecurityService(client)
    data = services.get_users()

    table = Table(title="OpenSearch Users")
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Backend Roles", style="magenta")
    table.add_column("Reserved", style="green")

    for name, info in data.items():
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
    data = services.get_health()
    print_json(data=data)


@security_app.command("whoami")
@handle_errors
def security_who_am_i(ctx: typer.Context):
    """Gets the identity information for the user currently logged in.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = SecurityService(client)
    data = services.who_am_i()
    print_json(data=data)


@policies_app.command("list-policies")
@handle_errors
def policies_list_policies(
    ctx: typer.Context,
    policy_id: Annotated[
        str | None, typer.Argument(help="Policy name (optional)")
    ] = None,
):
    """List all index policies

    Args:
        ctx (typer.Context): _description_
        policy_id (Annotated[ str  |  None, typer.Argument, optional): _description_. Defaults to "Policy name (optional)") ]=None.
    """
    client = get_client(ctx)
    services = PoliciesService(client)
    data = services.get_policy()
    print_json(data=data)


@policies_app.command("ensure")
@handle_errors
def policies_ensure_policy(
    ctx: typer.Context,
    policy_id: Annotated[str, typer.Argument(help="Policy ID")],
    file: typer.FileText = typer.Option(
        ..., "--file", "-f", help="Path to JSON-policy file"
    ),
):
    """Checks if policy already exists and create it if not

    Args:
        ctx (typer.Context): _description_
        policy_id (str, optional): _description_. Defaults to typer.Argument(..., help="Policy ID").
        file (typer.FileText, optional): _description_. Defaults to typer.Option( ..., "--file", "-f", help="Path to JSON-policy file" ).
    """
    client = get_client(ctx)
    services = PoliciesService(client)

    _, created = services.ensure_policy_exists()

    if created:
        console.print(f"Policy '{policy_id}' created", style="green")
    else:
        console.print(
            f"Policy '{policy_id}' already exists. No action required",
            style="blue",
        )


@tasks_app.command("get-task-info")
@handle_errors
def tasks_get_task_info(
    ctx: typer.Context,
    task_id: Annotated[str, typer.Argument(help="Task ID")],
):
    """Get information about task

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = TasksService(client, task_id=task_id)
    data = services.get_task_info()
    print_json(data=data)


@tasks_app.command("cancel-task")
@handle_errors
def tasks_cancel_task(
    ctx: typer.Context,
    task_id: Annotated[str, typer.Argument(help="Task ID")],
):
    """Cancel task by ID

    Args:
        ctx (typer.Context): _description_
        task_id (str, optional): _description_. Defaults to typer.Argument(None, help="Task ID").
    """
    client = get_client(ctx)
    services = TasksService(client, task_id=task_id)
    data = services.cancel_task()
    print_json(data=data)


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


@nodes_app.command("hot-thread")
@handle_errors
def nodes_get_hot_threads(
    ctx: typer.Context,
    node_id: Annotated[str | None, typer.Argument(help="Node ID")] = None,
    doc_type: Optional[str] = typer.Option(
        "cpu",
        "--doc_type",
        "-dt",
        help="The type to sample. Valid choices are {block, cpu, wait}",
    ),
):
    """Get hot threads

    Args:
        ctx (typer.Context): _description_
        node_id (Optional[str], optional): _description_. Defaults to typer.Argument(None, help="Node ID").
        doc_type (Optional[str], optional): _description_. Defaults to typer.Option( None, "--doc_type", "-dt", help="The type to sample. Valid choices are {block, cpu, wait}", ).
    """
    client = get_client(ctx)
    services = NodeService(client, node_id=node_id, doc_type=doc_type)
    filtered_lines = []
    found_start = False
    data = services.get_hot_threads()
    for line in data.splitlines():
        clean_line = line.strip()

        if "Hot threads" in clean_line:
            found_start = True

        if found_start:
            filtered_lines.append(line)

    result = "\n".join(filtered_lines)
    console.print(result.strip(), style="red")


@nodes_app.command("node-info")
@handle_errors
def nodes_get_node_info(
    ctx: typer.Context,
    node_id: Annotated[str | None, typer.Argument(help="Node ID")] = None,
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

    print_json(data=data)


@nodes_app.command("stats")
@handle_errors
def nodes_get_node_stats(
    ctx: typer.Context,
    node_id: Annotated[str | None, typer.Argument(help="Node ID")] = None,
    metric: Optional[str] = typer.Option(
        "_all",
        "--metric",
        "-m",
        help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list",
    ),
):
    """Get node stat

    Args:
        ctx (typer.Context): _description_
        node_id (Optional[str], optional): _description_. Defaults to typer.Argument(None, help="Node ID").
        metric (Optional[str], optional): _description_. Defaults to typer.Option( "_all", "--metric", "-m", help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list", ).

    """
    client = get_client(ctx)
    services = NodeService(client, node_id=node_id, metric=metric)

    data = services.get_node_stats()

    print_json(data=data)


@nodes_app.command("usage")
@handle_errors
def nodes_get_node_usage(
    ctx: typer.Context,
    node_id: Annotated[str | None, typer.Argument(help="Node ID")] = None,
    metric: Optional[str] = typer.Option(
        "_all",
        "--metric",
        "-m",
        help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list",
    ),
):
    """Get node usage

    Args:
        ctx (typer.Context): _description_
        node_id (Optional[str], optional): _description_. Defaults to typer.Argument(None, help="Node ID").
        metric (Optional[str], optional): _description_. Defaults to typer.Option( "_all", "--metric", "-m", help="Node metrics (settings, os, http, jvm, process, thread_pool, transport, plugins, ingest). Supports a comma-separated list", ).

    """
    client = get_client(ctx)
    services = NodeService(client, node_id=node_id, metric=metric)

    data = services.get_node_usage()

    print_json(data=data)


@user_friendly_cat_app.command("alias")
@handle_errors
def cat_get_alias(
    ctx: typer.Context,
    name: Annotated[
        str | None, typer.Argument(help="Alias name", show_default="All")
    ] = None,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. List Index Aliases

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, name=name, verbose=verbose)
    data = services.cat_alias()
    console.print(data)


@user_friendly_cat_app.command("allocation")
@handle_errors
def cat_get_allocation(
    ctx: typer.Context,
    node_id: Annotated[
        str | None, typer.Argument(help="Node ID", show_default="All")
    ] = None,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. Get Index Allocations

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, node_id=node_id, verbose=verbose)
    data = services.cat_allocation()
    console.print(data)


@user_friendly_cat_app.command("count")
@handle_errors
def cat_get_count(
    ctx: typer.Context,
    index: Annotated[
        str | None,
        typer.Argument(
            help="Index or alias. Supports a comma-separated list", show_default="All"
        ),
    ] = None,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. Count documents

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, index=index, verbose=verbose)
    data = services.cat_count()
    console.print(data)


@user_friendly_cat_app.command("fielddata")
@handle_errors
def cat_get_fielddata(
    ctx: typer.Context,
    fields: Annotated[
        str | None,
        typer.Argument(
            help="Field name. Supports a comma-separated list", show_default="All"
        ),
    ] = None,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. Count size of field name

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, fields=fields, verbose=verbose)
    data = services.cat_fielddata()
    console.print(data)


@user_friendly_cat_app.command("health")
@handle_errors
def cat_get_health(ctx: typer.Context):
    """EZ Cat. Get Cluster Health

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client)

    data = services.cat_health().strip().split("\n")
    if len(data) < 2:
        return

    headers, values = data[0].split(), data[1].split()
    stats = dict(zip(headers, values))

    column_config = [
        ("Cluster", "cluster", "white"),
        ("Status", "status", get_status_style(stats.get("status"))),
        ("Total nodes", "node.total", "green"),
        ("Data nodes", "node.data", "green"),
        ("Total Shards", "shards", "green"),
        ("Primary Shards", "pri", "green"),
        ("Relocating Shards", "relo", get_threshold_style(stats.get("relo"))),
        ("Initializing Shards", "init", "green"),
        ("Unassigned Shards", "unassign", get_threshold_style(stats.get("unassign"))),
        ("Pending tasks", "pending_tasks", "green"),
        ("Max wait", "max_task_wait_time", "green"),
        ("Active %", "active_shards_percent", "green"),
    ]

    table = Table(title="Cluster health")
    row_values = []

    for label, key, style in column_config:
        table.add_column(label, style=style)
        row_values.append(stats.get(key, "N/A"))

    table.add_row(*row_values)
    console.print(table)


@user_friendly_cat_app.command("indices")
@handle_errors
def cat_get_indices(
    ctx: typer.Context,
    index: Annotated[
        str | None,
        typer.Argument(
            help="Index name. Supports a comma-separated list.", show_default="All"
        ),
    ] = None,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT indices operation lists information related to indexes, that is, how much disk space they are using, how many shards they have, health status, etc.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, index=index, verbose=verbose)
    data = services.cat_indices()
    console.print(data)


@user_friendly_cat_app.command("cluster-manager")
@handle_errors
def cat_get_cluster_manager(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT cluster manager operation lists information that helps identify the elected cluster manager node.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_cluster_manager()
    console.print(data)


@user_friendly_cat_app.command("nodeattrs")
@handle_errors
def cat_get_nodeattrs(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT nodeattrs operation lists the attributes of custom nodes.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_nodeattrs()
    console.print(data)


@user_friendly_cat_app.command("nodes")
@handle_errors
def cat_get_nodes(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT nodes operation lists node-level information, including node roles and load metrics.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_nodes()
    console.print(data)


@user_friendly_cat_app.command("pending-tasks")
@handle_errors
def cat_get_pending_tasks(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT pending tasks operation lists the progress of all pending tasks, including task priority and time in queue.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_pending_tasks()
    console.print(data)


@user_friendly_cat_app.command("pit-segments")
@handle_errors
def cat_get_pit_segments(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT Point in Time (PIT) segments operation provides low-level information about the disk utilization

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_pit_segments()
    console.print(data)


@user_friendly_cat_app.command("plugins")
@handle_errors
def cat_get_plugins(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT plugins operation lists the names, components, and versions of the installed plugins.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_plugins()
    console.print(data)


@user_friendly_cat_app.command("recovery")
@handle_errors
def cat_get_recovery(
    ctx: typer.Context,
    index: Annotated[
        str | None,
        typer.Argument(
            help="Index name. Supports a comma-separated list.", show_default="All"
        ),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose")
    ] = False,
    is_active: Annotated[
        bool,
        typer.Option("--all", "-a", help="Show all operation list including finished"),
    ] = False,
):
    """EZ Cat. The CAT recovery operation lists all completed and ongoing index and shard recoveries.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose, is_active=is_active, index=index)
    data = services.cat_recovery()
    console.print(data)


@user_friendly_cat_app.command("repositories")
@handle_errors
def cat_get_repositories(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose",
    ),
):
    """EZ Cat. The CAT repositories operation lists all snapshot repositories for a cluster.

    Args:
        ctx (typer.Context): _description_
    """
    client = get_client(ctx)
    services = CatService(client, verbose=verbose)
    data = services.cat_repositories()
    console.print(data)


if __name__ == "__main__":
    app()
