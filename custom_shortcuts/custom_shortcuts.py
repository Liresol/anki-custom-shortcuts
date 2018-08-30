#Python 3.7.0
from aqt.main import AnkiQt
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from anki.hooks import runHook
from aqt.toolbar import Toolbar
from aqt.editor import Editor


#TODO: Change the toolbar & editor toolbar to reflect changed keys
#TODO: Make use of json
#TODO: Refactor code to minimize interaction between mw and the AnkiQt class

#Gets config.json as config
config = mw.addonManager.getConfig(__name__)


#There is a weird interaction with QShortcuts wherein if there are 2 (or more)
#QShortcuts mapped to the same key and function and both are enabled,
#the shortcut doesn't work

#Part of this code exploits that by adding QShortcuts mapped to the defaults
#and activating/deactivating them to deactivate/activate default shortcuts

#There isn't an obvious way to get the original QShortcut objects, as
#The addons executes after the setup phase (which creates QShortcut objects)

#Default shortcuts
mw.inversionSet =  [
    "Ctrl+:",
    "d",
    "s",
    "a",
    "b",
    "t",
    "y"
]

#List of "inverter" QShortcut objects that negate the defaults
mw.inverters = []

#Creates and inserts the inverter QShortcut objects
def cs_applyInverters():
    qshortcuts = []
    globalShortcuts = [
        ("Ctrl+:", mw.onDebug),
        ("d", lambda: mw.moveToState("deckBrowser")),
        ("s", mw.onStudyKey),
        ("a", mw.onAddCard),
        ("b", mw.onBrowse),
        ("t", mw.onStats),
        ("y", mw.onSync)
    ]
    for key, fn in globalShortcuts:
        scut = QShortcut(QKeySequence(key), mw, activated=fn)
        scut.setAutoRepeat(False)
        qshortcuts.append(scut)
        mw.inverters.append(scut)
    return qshortcuts

#Modified AnkiQt applyShortcuts to work around inverter shortcuts
#TODO: Be able to swap shortcut functions around
def _applyShortcuts(shortcuts):
    qshortcuts = []
    for key, fn in shortcuts:
        if key not in mw.inversionSet:
            scut = QShortcut(QKeySequence(key), mw, activated=fn)
            scut.setAutoRepeat(False)
            mw.shortcuts.append(scut)
            qshortcuts.append(scut)
        else:
            mw.inverters[mw.inversionSet.index(key)].setEnabled(False)
    return qshortcuts

#Initialize custom keys
def cs_initKeys():
    cuts = [
        config["debug"],
        config["deckbrowser"],
        config["study"],
        config["add"],
        config["browse"],
        config["stats"],
        config["sync"]
    ]
    functions =  [
        mw.onDebug,
        lambda: mw.moveToState("deckBrowser"),
        mw.onStudyKey,
        mw.onAddCard,
        mw.onBrowse,
        mw.onStats,
        mw.onSync
    ]
    globalShortcuts = list(zip(cuts,functions))
    _applyShortcuts(globalShortcuts)
    mw.keys = cuts
    mw.stateShortcuts = []

def _setupShortcuts(self):
    # if a third element is provided, enable shortcut even when no field selected
    cuts = [
        (config["card layout"], self.onCardLayout, True),
        (config["bold"], self.toggleBold),
        (config["italic"], self.toggleItalic),
        (config["underline"], self.toggleUnderline),
        (config["superscript"], self.toggleSuper),
        (config["subscript"], self.toggleSub),
        (config["remove format"], self.removeFormat),
        (config["foreground"], self.onForeground),
        (config["change col"], self.onChangeCol),
        (config["cloze"], self.onCloze),
        (config["cloze alt"], self.onCloze),
        (config["add media"], self.onAddMedia),
        (config["record sound"], self.onRecSound),
        (config["insert latex"], self.insertLatex),
        (config["insert latex equation"], self.insertLatexEqn),
        (config["insert latex math environment"], self.insertLatexMathEnv),
        (config["insert mathjax inline"], self.insertMathjaxInline),
        (config["insert mathjax block"], self.insertMathjaxBlock),
        (config["insert mathjax chemistry"], self.insertMathjaxChemistry),
        (config["html edit"], self.onHtmlEdit),
        (config["focus tags"], self.onFocusTags, True)
    ]
    runHook("setupEditorShortcuts", cuts, self)
    for row in cuts:
        if len(row) == 2:
            keys, fn = row
            fn = self._addFocusCheck(fn)
        else:
            keys, fn, _ = row
        scut = QShortcut(QKeySequence(keys), self.widget, activated=fn)

Editor.setupShortcuts = _setupShortcuts

mw.applyShortcuts = _applyShortcuts

cs_applyInverters()
cs_initKeys()
