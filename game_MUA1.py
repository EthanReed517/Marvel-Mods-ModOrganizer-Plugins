# -*- encoding: utf-8 -*-

from PyQt5.QtCore import QDir, QFileInfo, QStandardPaths

import mobase

from ..basic_game import BasicGame
from ..basic_features import BasicGameSaveGameInfo

class MarvelUltimateAllianceGame(BasicGame):
    Name = "Marvel - Ultimate Alliance Support Plugin"
    Author = "MrKablamm0fish and BaconWizard17"
    Version = "1.0.0"

    GameName = "Marvel - Ultimate Alliance"
    GameShortName = "mua1"
    GameNexusName = "mua1"
    GameNexusId = 000
    GameSteamId = 000000
    GameBinary = "game.exe"
    GameDataPath = ""
    GameSaveExtension = "save"
    GameDocumentsDirectory = "%DOCUMENTS%/Activision/Marvel Ultimate Alliance"
    GameSavesDirectory = "%GAME_DOCUMENTS%/Save"

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance",
                QFileInfo(self.gameDirectory(), "game.exe"),
            ),
        ]

