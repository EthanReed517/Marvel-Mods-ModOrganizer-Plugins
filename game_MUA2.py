# -*- encoding: utf-8 -*-

try:
  from PyQt5.QtCore import QFileInfo
except:
  from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame
from ..basic_features import BasicGameSaveGameInfo

class MarvelUltimateAllianceGame(BasicGame):
    Name = "Marvel - Ultimate Alliance 2 Support Plugin"
    Author = "MrKablamm0fish, ak2yny, Rampage, and BaconWizard17"
    Version = "2.0.0"

    GameName = "Marvel - Ultimate Alliance 2"
    GameShortName = "mua2"
    GameNexusName = "mua2"
    GameNexusId = 000
    GameSteamId = 433320
    GameBinary = "alliance.exe"
    GameDataPath = ""

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance 2",
                QFileInfo(self.gameDirectory(), "Alliance.exe"),
            ),
        ]

