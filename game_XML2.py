# -*- encoding: utf-8 -*-

from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame

class XML2ModDataChecker(mobase.ModDataChecker):
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

class XMenLegendsIIGame(BasicGame):
    Name = "X-Men Legends II Support Plugin"
    Author = "UltraMegaMagnus, ak2yny, Rampage, and BaconWizard17"
    Version = "2.1.0"

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

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(XML2ModDataChecker())
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "X-Men Legends II: Rise of Apocalypse",
                QFileInfo(self.gameDirectory(), "xmen2.exe"),
            ),
        ]
