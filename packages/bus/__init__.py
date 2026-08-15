import json, sqlite3
from pathlib import Path
from typing import Type
from pydantic import BaseModel
class EventBus:
    def __init__(self, path="data/swarm_events.sqlite"):
        Path(path).parent.mkdir(parents=True, exist_ok=True); self.db=sqlite3.connect(path); self.db.execute("create table if not exists swarm_events (topic text, payload text)")
    def publish(self, topic:str, payload:BaseModel): self.db.execute("insert into swarm_events values (?,?)",(topic,payload.model_dump_json())); self.db.commit()
    def replay(self, topic:str, model:Type[BaseModel]): return [model.model_validate_json(r[0]) for r in self.db.execute("select payload from swarm_events where topic=?",(topic,))]
