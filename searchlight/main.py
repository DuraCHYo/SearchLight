import typer
from rich.console import Console
from searchlight.core.cli import (
    security_app,
    policies_app,
    tasks_app,
    nodes_app,
    user_friendly_cat_app,
    main as common_callback,
)

app = typer.Typer()

app.callback()(common_callback)

app.add_typer(security_app, name="security", help="Manage users and roles")
app.add_typer(policies_app, name="policies", help="Manage index policies")
app.add_typer(tasks_app, name="tasks", help="Manage cluster tasks")
app.add_typer(nodes_app, name="nodes", help="Manage nodes")
app.add_typer(user_friendly_cat_app, name="cat", help="User Friendly APIs")

if __name__ == "__main__":
    app()
