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
            "data",
            "dialogs",
            "effects",
            "hud",
            "maps",
            "models",
            "motionpaths",
            "movies",
            "packages",
            "plugins",
            "scripts",
            "shaders",
            "skybox",
            "sounds",
            "subtitles",
            "texs",
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
    Name = "Marvel - Ultimate Alliance Support Plugin"
    Author = "MrKablamm0fish, ak2yny, Rampage, and BaconWizard17"
    Version = "2.1.0"

    GameName = "Marvel - Ultimate Alliance"
    GameShortName = "mua1"
    GameNexusName = "mua1"
    GameNexusId = 000
    GameSteamId = 000000
    GameBinary = "game.exe"
    GameLauncher = "MUA.exe"
    GameDataPath = ""
    GameSaveExtension = "save"
    GameDocumentsDirectory = "%DOCUMENTS%/Activision/Marvel Ultimate Alliance"
    GameSavesDirectory = "%GAME_DOCUMENTS%/Save"

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(MUA1ModDataChecker())
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance",
                QFileInfo(self.gameDirectory(), "game.exe"),
            ),
        ]

