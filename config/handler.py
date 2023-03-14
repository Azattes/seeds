import json
import logging
import pathlib
from datetime import date
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, List, Optional
from uuid import UUID

from mako.template import Template
from models import Seed
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
session = Session()

BASE_DIR = pathlib.Path(__file__).parent


class SeedIsAlreadyExecutedException(Exception):
    pass


class SeedValidationError(Exception):
    pass


class SeedInstance(BaseModel):
    id: str
    previous_seed_id: Optional[str] = None
    next_seed: Optional["SeedInstance"] = None

    @classmethod
    def from_module(cls, module: ModuleType) -> "SeedInstance":
        return SeedInstance(
            id=getattr(module, "seed_id"),
            previous_seed_id=getattr(module, "previous_seed"),
        )


class SeedList:
    def __init__(self, head: Optional[SeedInstance] = None):
        self.head = head

    def __iter__(self):
        node = self.head
        while node is not None:
            print(f"----- {node.id = } , {node.next_seed = }")
            yield node
            node = node.next_seed

    def add(self, node: SeedInstance):
        node.next_seed = self.head
        self.head = node

    def find(self, seed_id: str) -> Optional[SeedInstance]:
        current = self.head

        while current is not None:
            if current.id == seed_id:
                return current
            current = current.next_seed
        return None

    def find_by_previous(self, seed_id: str) -> Optional[SeedInstance]:
        current = self.head

        while current is not None:
            if current.previous_seed_id == seed_id:
                return current
            current = current.next_seed
        return None

    def sort(self) -> List[SeedInstance]:
        self._seeds = [self.head]
        previous_id = self.head.previous_seed_id
        while (previous := self.find(previous_id)) is not None:
            self._seeds.insert(0, previous)
            previous_id = previous.previous_seed_id

        latest = self._seeds[-1]
        next_id = latest.id

        while (next_ := self.find_by_previous(next_id)) is not None:
            self._seeds.append(next_)
            next_id = next_.id
        return self._seeds


class Runner:
    path = "scripts.{seed_id}"
    seed_list: SeedList = SeedList()

    async def create_file(self) -> pathlib.Path:
        file_path = BASE_DIR / "script.py.mako"
        template = Template(filename=str(file_path))
        try:
            latest_seed: Seed = await Seed.objects.order_by(
                "-created_at"
            ).first()
        except:
            latest_seed = None
        is_latest_seed = lambda x: x.id if x else None
        seed: Seed = await Seed.objects.create(
            previous_seed_id=is_latest_seed(latest_seed)
        )
        data = template.render(
            seed_id=seed.id,
            create_date=date.today(),
            previous_seed=is_latest_seed(latest_seed),
        ).replace("\n", "")

        path = self.get_path(seed_id=seed.id)
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(data)

        with open(BASE_DIR / "seeds.json", "r+") as f:
            data = json.load(f)
            data["seeds"].append(str(seed.id))
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        return path

    def get_path(self, seed_id: UUID):
        return BASE_DIR / "scripts" / "{seed_id}.py".format(seed_id=seed_id)

    def import_seed(self, seed_id: str):
        path = self.path.format(seed_id=seed_id)
        return import_module(path)

    async def run_seed(self, seed_id: UUID, validate: bool = True):
        try:
            module = self.import_seed(seed_id=seed_id)
            if validate:
                await self.validate(module)
            to_run: Callable[..., Any] = getattr(module, "seed")
            await to_run()
        except IntegrityError as e:
            print("ERROR: %s" % e)
            logging.error(e)
        else:
            await Seed.objects.filter(Seed.id == seed_id).update(
                is_executed=True
            )
            print(f"INFO: Seed {seed_id} was applied successfully.")
            logging.info("Seed %s was applied successfully.", seed_id)

    async def validate(self, module: ModuleType):
        if not hasattr(module, "previous_seed"):
            raise SeedValidationError(
                "ERROR: Seed has incorrect format. It must have the previous_seed attribute"  # noqa
            )

        previous_seed_id = getattr(module, "previous_seed")
        if previous_seed_id is not None:
            seed: Seed = await Seed.objects.filter(
                Seed.id == previous_seed_id
            ).first()
            if seed is None:
                raise SeedValidationError(
                    f"ERROR: Seed with id = {previous_seed_id} was not found!"
                )
            if not seed.is_executed:
                raise SeedValidationError(
                    "ERROR: Previous seed was not executed."
                )

    async def execute(self, seed_id=None):
        if seed_id is not None:
            await Seed.objects.get_or_create(id=seed_id)
            await self.run_seed(seed_id)
        else:
            with open(BASE_DIR / "seeds.json", "r") as f:
                data = json.load(f)
                for seed_id in data["seeds"]:
                    seed = SeedInstance.from_module(self.import_seed(seed_id))
                    uuid_seed_id = UUID(seed.id)
                    instance, _ = await Seed.objects.get_or_create(
                        id=uuid_seed_id
                    )
                    if not instance.is_executed:
                        await self.run_seed(
                            seed_id=uuid_seed_id, validate=False
                        )
