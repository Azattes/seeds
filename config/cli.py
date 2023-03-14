from typing import Optional

import asyncclick as click
from dependencies import get_database
from handler import Runner


@click.group()
def cli():
    pass


@click.command()
async def create():
    database = get_database()
    if not database.is_connected:
        await database.connect()
    runner = Runner()
    await runner.create_file()


@click.command()
@click.argument("seed_id", type=str, required=False)
async def execute(seed_id: Optional[str] = None):
    database = get_database()
    if not database.is_connected:
        await database.connect()
    runner = Runner()
    await runner.execute(seed_id=seed_id)


if __name__ == "__main__":
    cli.add_command(create)
    cli.add_command(execute)
    cli(_anyio_backend="asyncio")
