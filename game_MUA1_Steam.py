# -*- encoding: utf-8 -*-

try:
  from PyQt5.QtCore import QFileInfo
except:
  from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame
from ..basic_features import BasicGameSaveGameInfo

class MarvelUltimateAllianceGame(BasicGame):
    Name = "Marvel - Ultimate Alliance (Steam Version) Support Plugin"
    Author = "MrKablamm0fish, ak2yny, and BaconWizard17"
    Version = "2.0.0"

    GameName = "Marvel - Ultimate Alliance (Steam)"
    GameShortName = "mua1s"
    GameNexusName = "mua1s"
    GameNexusId = 000
    GameSteamId = 433300
    GameBinary = "marvel.exe"
    GameDataPath = ""

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance (Steam)",
                QFileInfo(self.gameDirectory(), "Marvel.exe"),
            ),
        ]
