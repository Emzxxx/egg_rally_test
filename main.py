from controller import Controller
from model import Model
from view import View
import json

def main() -> None:
    with open("settings.json") as f:
        settings = json.load(f)

    model = Model(settings)
    view = View(settings["world_width"], settings["world_height"])
    controller = Controller(model, view)
    view.start(settings["fps"], controller.update, controller.draw)

if __name__ == "__main__":
    main()