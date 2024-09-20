# -*- encoding: utf-8 -*-
from collections.abc import Mapping
from pathlib import Path

from PyQt6.QtCore import QFileInfo, QDateTime, QDir

import mobase
from ..basic_game import BasicGame
from ..basic_features import BasicLocalSavegames
from ..basic_features.basic_save_game_info import (
    BasicGameSaveGame,
    BasicGameSaveGameInfo,
    format_date,
)

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

class XML2SaveGame(BasicGameSaveGame):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

        head_length = 0x00000080
        size_length = 0x00000004

        with open(self._filepath, "rb") as sbin:
            head = sbin.read(head_length).split(b'\x00')[0].decode()
            # size = int.from_bytes(sbin.read(size_length), "little")
            # save = sbin.read(size)
            # sbin.close()
        # info = save.split(b'\x0a')[1].split(b'\x00')[0].decode()

        self._name = head.split(' - ')[1].split('(')[0].strip()
        self._difficulty = head.split()[-1][1:-1]
        self._elapsed = head.split(' - ')[0]
        f_stat = self._filepath.stat()
        self._created = f_stat.st_birthtime
        self._modified = f_stat.st_mtime

    def getName(self) -> str:
        return self._name

    def getCreationTime(self) -> QDateTime:
        return QDateTime.fromSecsSinceEpoch(int(self._created))

    def getModifiedTime(self) -> QDateTime:
        return QDateTime.fromSecsSinceEpoch(int(self._modified))

    def getDifficulty(self) -> str:
        return self._difficulty

    def getElapsed(self) -> str:
        return self._elapsed

def getMetadata(savepath: Path, save: mobase.ISaveGame) -> Mapping[str, str]:
    assert isinstance(save, XML2SaveGame)
    return {
        "Extraction Point": save.getName(),
        "Difficulty": save.getDifficulty(),
        "Last Saved": format_date(save.getModifiedTime()),
        "Created At": format_date(save.getCreationTime()),
        "Elapsed time": save.getElapsed(),
    }


class XMenLegendsIIGame(BasicGame):
    Name = "X-Men Legends II Support Plugin"
    Author = "UltraMegaMagnus, ak2yny, Rampage, and BaconWizard17"
    Version = "2.2.0"

    GameName = "X-Men Legends II - Rise of Apocalypse"
    GameShortName = "xml2"
    GameNexusName = "xml2"
    GameNexusId = 000
    GameSteamId = 000000
    GameBinary = "xmen2.exe"
    GameDataPath = ""
    GameDocumentsDirectory = "%DOCUMENTS%/Activision/X-Men Legends 2"
    GameSavesDirectory = "%GAME_DOCUMENTS%/Save"
    GameSaveExtension = "save"
    GameSupportURL = "https://github.com/EthanReed517/Marvel-Mods-ModOrganizer-Plugins"

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(XML2ModDataChecker())
        self._register_feature(BasicLocalSavegames(self.savesDirectory()))
        self._register_feature(
            BasicGameSaveGameInfo(get_metadata=getMetadata, max_width=400)
        )
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "X-Men Legends II: Rise of Apocalypse",
                QFileInfo(self.gameDirectory(), "xmen2.exe"),
            ),
        ]

    def listSaves(self, folder: QDir) -> list[mobase.ISaveGame]:
        ext = self._mappings.savegameExtension.get()
        return [
            XML2SaveGame(path) for path in Path(folder.absolutePath()).glob(f"*.{ext}") # e.g. saveslot0.save
        ]
