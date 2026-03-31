import typer
from cli import security_app, policies_app, main as common_callback

app = typer.Typer()

app.callback()(common_callback)

app.add_typer(security_app, name="security", help="Manage users and roles")
app.add_typer(policies_app, name="policies", help="Manage index policies")

if __name__ == "__main__":
    app()
