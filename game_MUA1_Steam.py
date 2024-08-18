# -*- encoding: utf-8 -*-

from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame

class MUA1ModDataChecker(mobase.ModDataChecker):
    def __init__(self):
        super().__init__()
        self.validDirNames = [
            "actors",
            "automaps",
            "conversations",
            "cursors",
            "data",
            "dialogs",
            "effects",
            "eula",
            "hud",
            "maps",
            "models",
            "motionpaths",
            "movies",
            "packages",
            "plugins",
            "SavesDir",
            "scripts",
            "Settings",
            "shaders",
            "skybox",
            "sounds",
            "subtitles",
            "textures",
            "ui"
        ]

    def dataLooksValid(
        self, tree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        for entry in tree:
            if not entry.isDir():
                continue
            if entry.name().casefold() in self.validDirNames:
                return mobase.ModDataChecker.VALID
        return mobase.ModDataChecker.INVALID

class MarvelUltimateAllianceGame(BasicGame):
    Name = "Marvel - Ultimate Alliance (Steam Version) Support Plugin"
    Author = "MrKablamm0fish, ak2yny, Rampage, and BaconWizard17"
    Version = "2.1.0"

    GameName = "Marvel - Ultimate Alliance (Steam)"
    GameShortName = "mua1s"
    GameNexusName = "mua1s"
    GameNexusId = 000
    GameSteamId = 433300
    GameBinary = "marvel.exe"
    GameDataPath = ""
    GameSaveExtension = "sav"
    GameDocumentsDirectory = "%USERPROFILE%/AppData/Roaming/Activision/Marvel Ultimate Alliance"
    GameSavesDirectory = "%GAME_PATH%/SavesDir"

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(MUA1ModDataChecker())
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance (Steam)",
                QFileInfo(self.gameDirectory(), "Marvel.exe"),
            ),
        ]
