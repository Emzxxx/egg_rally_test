import json
from model import GameModel
from view import GameView
from controller import GameController
from typing import Any

def main():
    with open("settings.json") as f:
        settings: dict[str, Any] = json.load(f)

    model = GameModel(settings)
    view = GameView(model.width, model.height)
    controller = GameController(model, view)

    controller.start()

if __name__ == "__main__":
    main()
