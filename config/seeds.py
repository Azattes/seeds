from typing import Optional

import typer
from handler import Runner
from utils import coro

app = typer.Typer()


@app.command()
@coro
async def execute(seed_id: Optional[str] = None):
    runner = Runner()
    await runner.execute(seed_id=seed_id)


@app.command()
@coro
async def create():
    runner = Runner()
    await runner.create_file()


if __name__ == "__main__":
    app()
