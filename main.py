import json
from model import GameModel
from view import GameView
from controller import GameController
from typing import Any
from project_types import Eggnemy_Spawner, Boss_Spawner

def main():
    with open("settings.json") as f:
        settings: dict[str, Any] = json.load(f)

    model = GameModel(settings, Eggnemy_Spawner(), Boss_Spawner())
    view = GameView(model.width, model.height)
    controller = GameController(model, view)

    controller.start()

if __name__ == "__main__":
    main()
