# This plugin is based on the FNIS plugin for MO2 by AnyOldName3.

# To use this plugin, place it in the plugins directory of your Mod Organizer install. You will then find the '' and '' options under the tools menu.

# Intended behaviour:
# * Adds buttons to tools menu.
# * If herostats mod isn't known (or isn't valid, e.g. isn't actually there) when the button is pressed, a file chooser is displayed to select one.
# * A helpful popup saying whether or not the patch worked.

from pathlib import Path
from typing import List
import sys, time, zipfile

from PyQt6.QtCore import qCritical, QFileInfo #, QCoreApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QMessageBox

import mobase

# If the patch files would be used from remote sources, we could use the urllib
# import urllib.request

P_NAME = "XML2 Tools"
P_HSPATCH = "XML2 Patch Hs"
P_AUTHOR = "ak2yny"
P_VERSION = mobase.VersionInfo(1, 2, 0, 0)
#return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.FINAL)
P_REQ = {
    "BasicGame",
    "X-Men Legends II - Rise of Apocalypse"
}
P_ICON = "xml2.ico"
ZIP_FILE = "plugins/XML2Patch.zip"

def tr(str) -> str:
    #translations not implemented:
    #return QCoreApplication.translate("XML2Tools", str)
    #XML2Tools.tr(str)
    return str

MSG_MODFOLDER_T = tr("Herostat mod not set")
MSG_MODFOLDER = tr("The herostat mod was not specified. The tool will now exit.")
MSG_BROKEN_T = tr("Broken game")
MSG_BROKEN = tr("No new_game.py file found. Is the game setup broken? A re-installation of XML2 or new setup of MO2 might be required.")
MSG_MISSING_T = tr("File not found error")
MSG_MISSING = tr(f"The patch was not found in '{ZIP_FILE}'. Please re-install the XML2 plugin for MO2.\nIt's possible that an anti-virus program removed the .zip. In this case, disable protection temporarily, re-install the plugin, add '{ZIP_FILE}' to exclusions in the anti-virus and re-enable protection.")
MSG_ACCESS_T = tr("Permission denied")
MSG_ACCESS = tr(f"This can happen, if the game is in program files, in which case it helps to move it to an unprotected location, such as 'C:/Games'. Otherwise, it might be possible to give MO2 and Python write permission to the game folder through file explorer.\nIt's also possible that an anti-virus program prevents the patch from working. To allow it, briefly disable protection while patching. If necessary, add the patched xmen2.exe to the exceptions afterwards. Don't forget to turn protection back on.\nIn any case, you can also manually extract xmen2.exe from '{ZIP_FILE}' to ")
MSG_FAIL_T = tr("Extraction error")
MSG_FAIL = tr("Extraction of the patch files failed. Please follow the tutorials and ask for help if necessary.")

class UnknownOutputPreferenceException(Exception):
    """Thrown if the user hasn't specified whether to output to a separate mod"""
    pass

class XML2Tools(mobase.IPluginTool):

    def __init__(self):
        super(XML2Tools, self).__init__()
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
        return tr("Patch the game for use with MO2 and OHS.")

    def version(self):
        return P_VERSION

    def requirements(self):
        return [
            mobase.PluginRequirementFactory.gameDependency(P_REQ)
        ]

    def settings(self):
        return [
            mobase.PluginSetting("patch-hs", tr("Patch the herostat mod to work with OHS."), True),
            mobase.PluginSetting("patch-ex", tr("Patch the game's .exe to work on Windows."), True)
        ]

    def displayName(self):
        return tr("XML2 Patch All")

    def tooltip(self):
        return tr("Patches the game so that it starts and OHS works as expected.")

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

            # Copy the new_game that's used by this profile, currently
            if not patchHerostatMod(self.__organizer, herostatModPath):
                QMessageBox.critical(self.__parentWidget, MSG_BROKEN_T, MSG_BROKEN)
                return

            # Enable the herostat mod
            self.__organizer.modList().setActive(herostatModPath.name, True)
            modCount = len(self.__organizer.modList().allMods())
            self.__organizer.modList().setPriority(herostatModPath.name, modCount)

        if bool(self.__organizer.pluginSetting(self.name(), "patch-ex")):
            # Extract the roster hack files to the game directory
            game_dir = self.__organizer.managedGame().dataDirectory().absolutePath()
            try:
                patchGameFolder(game_dir)
                QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Game files patched successfully."))
            except FileNotFoundError:
                QMessageBox.critical(self.__parentWidget, MSG_MISSING_T, MSG_MISSING)
            except PermissionError as e:
                QMessageBox.critical(self.__parentWidget, MSG_ACCESS_T, f"{e}\n{MSG_ACCESS}'{game_dir}'.")
            except:
                QMessageBox.critical(self.__parentWidget, MSG_FAIL_T, MSG_FAIL)

class XML2PatchRH(mobase.IPluginTool):

    def __init__(self):
        super(XML2PatchRH, self).__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "XML2 Patch Game"

    def localizedName(self):
        return tr("XML2 Patch Game")

    def author(self):
        return P_AUTHOR

    def description(self):
        return tr("Patch the game for use with MO2.")

    def version(self):
        return P_VERSION

    def requirements(self):
        return [
            mobase.PluginRequirementFactory.gameDependency(P_REQ)
        ]

    def settings(self):
        return []

    def displayName(self):
        return tr("XML2 Patch Game")

    def tooltip(self):
        return tr("Patches the game so that it starts.")

    def icon(self):
        return QIcon(self.__organizer.managedGame().dataDirectory().absoluteFilePath(P_ICON))

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        # Extract the cracked .exe to the game directory
        game_dir = self.__organizer.managedGame().dataDirectory().absolutePath()
        try:
            patchGameFolder(game_dir)
            QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Game files patched successfully."))
        except FileNotFoundError:
            QMessageBox.critical(self.__parentWidget, MSG_MISSING_T, MSG_MISSING)
        except PermissionError as e:
            QMessageBox.critical(self.__parentWidget, MSG_ACCESS_T, f"{e}\n{MSG_ACCESS}'{game_dir}'.")
        except:
            QMessageBox.critical(self.__parentWidget, MSG_FAIL_T, MSG_FAIL)

class XML2PatchHerostat(mobase.IPluginTool):

    def __init__(self):
        super(XML2PatchHerostat, self).__init__()
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
        return tr("XML2 Patch Herostat Mod")

    def tooltip(self):
        return tr("Patches the herostat mod so that OHS works as expected.")

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

        # Copy the new_game that's used by this profile, currently
        if not patchHerostatMod(self.__organizer, herostatModPath):
            QMessageBox.critical(self.__parentWidget, MSG_BROKEN_T, MSG_BROKEN)
            return

        # Enable the herostat mod
        self.__organizer.modList().setActive(herostatModPath.name, True)
        modCount = len(self.__organizer.modList().allMods())
        self.__organizer.modList().setPriority(herostatModPath.name, modCount)

        QMessageBox.information(self.__parentWidget, tr("Success!"), tr("Herostat mod patched successfully."))

def patchGameFolder(gamePath: str):
    # ZIP_FILE, headers = urllib.request.urlretrieve('https://github.com/EthanReed517/Marvel-Mods-ModOrganizer-Plugins/raw/refs/heads/main/XML2/XML2Patch.zip')
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(gamePath)
    # urllib.request.urlcleanup()

def patchHerostatMod(mo, herostatMod: Path) -> bool:
    files = mo.findFiles(Path('scripts/menus').as_posix(), 'new_game*.py')
    if not files: return False
    for p in files:
        oldNewGame = Path(p)
        newNewGame = herostatMod / 'scripts' / 'menus' / oldNewGame.name
        bkpNewGame = herostatMod / 'scripts' / 'menus' / f'{oldNewGame.name}.backup{oldNewGame.suffix}'
        if oldNewGame == newNewGame: continue
        if newNewGame.exists(): newNewGame.replace(bkpNewGame)
        else: newNewGame.parent.mkdir(parents=True, exist_ok=True)
        newNewGame.write_bytes(oldNewGame.read_bytes())
    # Make sure a 'data' folder exist
    dataPath = herostatMod / 'data'
    dataPath.mkdir(exist_ok=True)
    return True

def getOutputPath(mo, widget) -> Path:
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

    # Disable the herostat mod temporarily to fix the VFS
    mo.modList().setActive(pathlibPath.name, True)

    # The user may have created a new mod in the MO2 mods directory, so we must trigger a refresh
    mo.refresh()
    mo.setPluginSetting(P_HSPATCH, "output-path", path)

    return pathlibPath

def createPlugins() -> List[mobase.IPlugin]:
    return [XML2Tools(), XML2PatchRH(), XML2PatchHerostat()]
