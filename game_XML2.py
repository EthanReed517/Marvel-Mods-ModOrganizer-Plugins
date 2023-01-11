# -*- encoding: utf-8 -*-

from PyQt5.QtCore import QDir, QFileInfo, QStandardPaths

import mobase

from ..basic_game import BasicGame
from ..basic_features import BasicGameSaveGameInfo

class XMenLegendsIIGame(BasicGame):
    Name = "X-Men Legends II: Rise of Apocalypse"
    Author = "UltraMegaMagnus"
    Version = "0.0.2"

    GameName = "X-Men Legends II: Rise of Apocalypse"
    GameShortName = "xml2"
    GameNexusName = "xml2"
    GameBinary = "xmen2.exe"
    GameDataPath = ""
    GameSaveExtension = "save"
    GameDocumentsDirectory = r"%DOCUMENTS%/Activision/X-Men Legends 2"
    GameSavesDirectory = r"%GAME_DOCUMENTS%/Save"

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "X-Men Legends II: Rise of Apocalypse",
                QFileInfo(self.gameDirectory(), "xmen2.exe"),
            ),
        ]

