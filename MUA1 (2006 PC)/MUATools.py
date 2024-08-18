# This plugin is based on the FNIS plugin for MO2 by AnyOldName3.

# To use this plugin, place it in the plugins directory of your Mod Organizer install. You will then find the '' and '' options under the tools menu.

# Intended behaviour:
# * Adds buttons to tools menu.
# * If herostats mod isn't known (or isn't valid, e.g. isn't actually there) when the button is pressed, a file chooser is displayed to select one.
# * A helpful popup saying whether or not the patch worked.

from pathlib import Path
from typing import List

from PyQt6.QtCore import qCritical, QFileInfo #, QCoreApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QMessageBox

import sys
import mobase
import zipfile
import time

# If the patch files would be used from remote sources, we could use the urllib
# import urllib.request

P_NAME = "MUA Tools"
P_HSPATCH = "MUA Patch Hs"
P_AUTHOR = "ak2yny"
P_VERSION = mobase.VersionInfo(1, 0, 1, 0)
#return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.FINAL)
P_REQ = {
    "BasicGame",
    "Marvel Ultimate Alliance" # "Marvel - Ultimate Alliance"
}
P_ICON = "MUA.ico"

def tr(str) -> str:
    #translations not implemented:
    #return QCoreApplication.translate("MUATools", str)
    #MUATools.tr(str)
    return str

MSG_MODFOLDER_T = tr("Herostat mod not set")
MSG_MODFOLDER = tr("The herostat mod was not specified. The tool will now exit.")
MSG_BROKEN_T = tr("Broken game")
MSG_BROKEN = tr("No new_game.py file found. Is the game setup broken? A re-installation of MUA or new setup of MO2 might be required.")
MSG_ACCESS_T = tr("Access error")
MSG_ACCESS = tr("Extraction of the patch files failed. Please follow the tutorials and ask for help, if necessary.")

class UnknownOutputPreferenceException(Exception):
    """Thrown if the user hasn't specified whether to output to a separate mod"""
    pass

class MUATools(mobase.IPluginTool):

    def __init__(self):
        super(MUATools, self).__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        if sys.version_info < (3, 0):
            qCritical(tr("Plugin requires a Python 3 interpreter, but is running on a Python 2 interpreter."))
            QMessageBox.critical(self.__parentWidget, tr("Incompatible Python version."), tr("This plugin requires a Python 3 interpreter, but Mod Organizer has provided a Python 2 interpreter. Please update Mod Organizer 2."))
            return False
        return True

    def name(self):
        return P_NAME

    def localizedName(self):
        return tr(P_NAME)

    def author(self):
        return P_AUTHOR

    def description(self):
        return tr("Patch the game for use with MO2, OHS and the roster hacks.")

    def version(self):
        return P_VERSION

    def requirements(self):
        return [
            mobase.PluginRequirementFactory.gameDependency(P_REQ)
        ]

    def settings(self):
        return [
            mobase.PluginSetting("patch-hs", tr("Patch the herostat mod to work with OHS."), True),
            mobase.PluginSetting("patch-rh", tr("Patch the game files to work with MO2."), True)
        ]

    def displayName(self):
        return tr("MUA Patch All")

    def tooltip(self):
        return tr("Patches the game, so the roster hacks, debug menu and OHS work as expected.")

    def icon(self):
        return QIcon(self.__organizer.managedGame().dataDirectory().absoluteFilePath(P_ICON))

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        if bool(self.__organizer.pluginSetting(self.name(), "patch-hs")):
            herostatModPath = None

            try:
                herostatModPath = getOutputPath(self.__organizer, self.__parentWidget)
            except UnknownOutputPreferenceException:
                QMessageBox.critical(self.__parentWidget, MSG_MODFOLDER_T, MSG_MODFOLDER)
                return

            self.__organizer.setPluginSetting(P_HSPATCH, "initialised", True)
            time.sleep(0.2)

            # Enable the herostat mod
            self.__organizer.modList().setActive(herostatModPath.name, True)
            modCount = len(self.__organizer.modList().allMods())
            self.__organizer.modList().setPriority(herostatModPath.name, modCount)

            # Copy the new_game that's used by this profile, currently
            parent = Path('scripts/menus').as_posix()
            files = self.__organizer.findFiles(parent, 'new_game.py')
            if files:
                patchHerostatMod(herostatModPath, Path(files[0]))
            else:
                QMessageBox.critical(self.__parentWidget, MSG_BROKEN_T, MSG_BROKEN)
                return

        if bool(self.__organizer.pluginSetting(self.name(), "patch-rh")):
            # Extract the roster hack files to the game directory
            try:
                patchGameFolder(self.__organizer.managedGame().dataDirectory().absolutePath())
            except:
                QMessageBox.critical(self.__parentWidget, MSG_ACCESS_T, MSG_ACCESS)
                return

        QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Game files patched successfully."))

class MUAPatchRH(mobase.IPluginTool):

    def __init__(self):
        super(MUAPatchRH, self).__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "MUA Patch RH"

    def localizedName(self):
        return tr("MUA Patch RH")

    def author(self):
        return P_AUTHOR

    def description(self):
        return tr("Patch the game for use with MO2 and the roster hacks.")

    def version(self):
        return P_VERSION

    def requirements(self):
        return [
            mobase.PluginRequirementFactory.gameDependency(P_REQ)
        ]

    def settings(self):
        return []

    def displayName(self):
        return tr("MUA Patch RH")

    def tooltip(self):
        return tr("Patches the game, so the roster hacks and debug menu work as expected.")

    def icon(self):
        return QIcon(self.__organizer.managedGame().dataDirectory().absoluteFilePath(P_ICON))

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        # Extract the roster hack files to the game directory
        try:
            patchGameFolder(self.__organizer.managedGame().dataDirectory().absolutePath())
        except:
            QMessageBox.critical(self.__parentWidget, MSG_ACCESS_T, MSG_ACCESS)
            return

        QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Game files patched successfully."))

class MUAPatchHerostat(mobase.IPluginTool):

    def __init__(self):
        super(MUAPatchHerostat, self).__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return P_HSPATCH

    def localizedName(self):
        return tr(P_HSPATCH)

    def author(self):
        return P_AUTHOR

    def description(self):
        return tr("Patch this MO2 profile for use with OHS.")

    def version(self):
        return P_VERSION

    def requirements(self):
        return [
            mobase.PluginRequirementFactory.gameDependency(P_REQ)
        ]

    def settings(self):
        return [
            mobase.PluginSetting("initialised", tr("Settings have been initialised. Set to False to reinitialise them."), False),
            mobase.PluginSetting("output-path", tr("The path to the herostat mod."), ""),
        ]

    def displayName(self):
        return tr("MUA Patch Herostat Mod")

    def tooltip(self):
        return tr("Patches the herostat mod, so OHS works as expected.")

    def icon(self):
        return QIcon(self.__organizer.managedGame().dataDirectory().absoluteFilePath(P_ICON))

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        herostatModPath = None

        try:
            herostatModPath = getOutputPath(self.__organizer, self.__parentWidget)
        except UnknownOutputPreferenceException:
            QMessageBox.critical(self.__parentWidget, MSG_MODFOLDER_T, MSG_MODFOLDER)
            return

        self.__organizer.setPluginSetting(self.name(), "initialised", True)
        time.sleep(0.2)

        # Enable the herostat mod
        self.__organizer.modList().setActive(herostatModPath.name, True)
        modCount = len(self.__organizer.modList().allMods())
        self.__organizer.modList().setPriority(herostatModPath.name, modCount)

        # Copy the new_game that's used by this profile, currently
        parent = Path('scripts/menus').as_posix()
        files = self.__organizer.findFiles(parent, 'new_game.py')
        if files:
            patchHerostatMod(herostatModPath, Path(files[0]))
        else:
            QMessageBox.critical(self.__parentWidget, MSG_BROKEN_T, MSG_BROKEN)
            return

        QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Herostat mod patched successfully."))

def patchGameFolder(gamePath: str):
    # zip_file, headers = urllib.request.urlretrieve('https://github.com/.../.../releases/latest/download/....zip')
    zip_file = "plugins/MUAPatch.zip"
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(gamePath)
    # urllib.request.urlcleanup()

def patchHerostatMod(herostatMod: Path, oldNewGame: Path):
    newNewGame = herostatMod / 'scripts' / 'menus' / 'new_game.py'
    newNewGame.parent.mkdir(parents=True, exist_ok=True)
    newNewGame.write_bytes(oldNewGame.read_bytes())
    # Make sure a 'data' folder exist
    dataPath = herostatMod / 'data'
    dataPath.mkdir(exist_ok=True)

def getOutputPath(mo, widget):
    path = mo.pluginSetting(P_HSPATCH, "output-path") if bool(mo.pluginSetting(P_HSPATCH, "initialised")) else ""
    pathlibPath = Path(path)
    modDirectory = mo.modsPath()
    isAMod = pathlibPath.parent.samefile(modDirectory)
    if not pathlibPath.is_dir() or not isAMod:
        QMessageBox.information(widget, tr("Select the herostat mod"), tr("Please choose the mod that you use for OHS. This must be a directory in Mod Organizer 2's mods directory, and you can create one if you do not have one already. This setting can be updated in the Plugins tab of the Mod Organizer 2 Settings menu."))
        while not pathlibPath.is_dir() or not isAMod:
            path = QFileDialog.getExistingDirectory(widget, tr("Select the herostat mod"), str(modDirectory), QFileDialog.Option.ShowDirsOnly)
            if not path:
                # cancel was pressed
                raise UnknownOutputPreferenceException
            pathlibPath = Path(path)
            isAMod = pathlibPath.parent.samefile(modDirectory)
            if not isAMod:
                QMessageBox.information(widget, tr("Not a mod..."), tr("The selected directory is not a Mod Organizer managed mod. Please choose a directory within the mods directory."))
                continue
        # The user may have created a new mod in the MO2 mods directory, so we must trigger a refresh
        mo.refreshModList()
        mo.setPluginSetting(P_HSPATCH, "output-path", path)

    return pathlibPath

def createPlugins() -> List[mobase.IPlugin]:
    return [MUATools(), MUAPatchRH(), MUAPatchHerostat()]
