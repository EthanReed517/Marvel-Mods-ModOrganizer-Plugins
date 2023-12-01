# -*- encoding: utf-8 -*-

try:
  from PyQt5.QtCore import QFileInfo
except:
  from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame
from ..basic_features import BasicGameSaveGameInfo

class XMenLegendsIIGame(BasicGame):
    Name = "X-Men Legends II Support Plugin"
    Author = "UltraMegaMagnus, ak2yny, and BaconWizard17"
    Version = "2.0.0"

    GameName = "X-Men Legends II - Rise of Apocalypse"
    GameShortName = "xml2"
    GameNexusName = "xml2"
    GameNexusId = 000
    GameSteamId = 000000
    GameBinary = "xmen2.exe"
    GameDataPath = ""
    GameSaveExtension = "save"
    GameDocumentsDirectory = "%DOCUMENTS%/Activision/X-Men Legends 2"
    GameSavesDirectory = "%GAME_DOCUMENTS%/Save"

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "X-Men Legends II: Rise of Apocalypse",
                QFileInfo(self.gameDirectory(), "xmen2.exe"),
            ),
        ]

