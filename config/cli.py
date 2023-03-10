import typer

import seeds as seeds

app = typer.Typer()


app.add_typer(seeds.app, name="seed")

if __name__ == "__main__":
    app()
