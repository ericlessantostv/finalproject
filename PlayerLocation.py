from dataclasses import dataclass
import datetime
from typing import Dict


from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class PlayerLocation:
    x_loc: int
    y_loc: int
    points: int
    last_update: datetime.datetime

@dataclass_json
@dataclass
class GameState:
    player_states: Dict[str, PlayerLocation]
