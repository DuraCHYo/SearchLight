import typer
from cli import (
    security_app,
    policies_app,
    tasks_app,
    nodes_app,
    main as common_callback,
)

app = typer.Typer()

app.callback()(common_callback)

app.add_typer(security_app, name="security", help="Manage users and roles")
app.add_typer(policies_app, name="policies", help="Manage index policies")
app.add_typer(tasks_app, name="tasks", help="Manage cluster tasks")
app.add_typer(nodes_app, name="nodes", help="Manage nodes")


if __name__ == "__main__":
    app()
