# -*- encoding: utf-8 -*-

from PyQt6.QtCore import QFileInfo

import mobase
from ..basic_game import BasicGame

class MUA2ModDataChecker(mobase.ModDataChecker):
    def __init__(self):
        super().__init__()
        self.validDirNames = [
            "actors",
            "anims",
            "animTranslationReference",
            "ArchiveInputFiles",
            "chatter",
            "conversations",
            "cursors",
            "data",
            "dialogs",
            "effects_igx",
            "maps",
            "materials",
            "models",
            "motionpaths",
            "movies",
            "packages",
            "ragdoll",
            "SavesDir",
            "scripts",
            "Settings",
            "shaders",
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
    Name = "Marvel - Ultimate Alliance 2 Support Plugin"
    Author = "MrKablamm0fish, ak2yny, Rampage, and BaconWizard17"
    Version = "2.1.0"

    GameName = "Marvel - Ultimate Alliance 2"
    GameShortName = "mua2"
    GameNexusName = "marvelultimatealliance2"
    GameNexusId = 000
    GameSteamId = 433320
    GameBinary = "alliance.exe"
    GameDataPath = ""
    GameSaveExtension = "sav"
    GameSavesDirectory = "%GAME_PATH%/SavesDir"

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(MUA2ModDataChecker())
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Marvel: Ultimate Alliance 2",
                QFileInfo(self.gameDirectory(), "Alliance.exe"),
            ),
        ]

