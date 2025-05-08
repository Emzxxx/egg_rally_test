import json
import pyxel
from model import GameModel
from view import GameView
from controller import GameController


class EggRallyApp:
    def __init__(self):
        with open("settings.json") as f:
            self.settings = json.load(f)

        pyxel.init(self.settings["world_width"], self.settings["world_height"], fps=self.settings["fps"], title="Egg Rally")

        self.model = GameModel(self.settings)
        self.view = GameView(self.model)
        self.controller = GameController(self.model)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.controller.update()

    def draw(self):
        self.view.draw()


if __name__ == "__main__":
    EggRallyApp()