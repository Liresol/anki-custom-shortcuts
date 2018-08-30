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

config = mw.addonManager.getConfig(__name__)


mw.inversionSet =  [
    "Ctrl+:",
    "d",
    "s",
    "a",
    "b",
    "t",
    "y"
]

mw.shortcuts = []
mw.inverters = []

def applyInverters():
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



def _setupKeys():
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
    #prevGlobalShortcuts = list(zip(mw.keys,functions))
    globalShortcuts = list(zip(cuts,functions))

    #self.applyShortcuts(prevGlobalShortcuts)
    _applyShortcuts(globalShortcuts)
    mw.keys = cuts
    mw.stateShortcuts = []

"""
mw.editorCuts = [
"Ctrl+L",
"Ctrl+B",
"Ctrl+I",
"Ctrl+U",
"Ctrl++",
"Ctrl+=",
"Ctrl+R",
"F7",
"F8",
"Ctrl+Shift+C",
"Ctrl+Shift+Alt+C",
"F3",
"F5",
"Ctrl+T, T",
"Ctrl+T, E",
"Ctrl+T, M",
"Ctrl+M, M",
"Ctrl+M, E",
"Ctrl+M, C",
"Ctrl+Shift+X",
"Ctrl+Shift+T",
]
"""


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
    """
    for row in prevCuts:
    if len(row) == 2:
    keys, fn = row
    else:
    keys, fn, _ = row
    QShortcut(QKeySequence(keys), self.widget, activated=fn)
    """
    for row in cuts:
        if len(row) == 2:
            keys, fn = row
            fn = self._addFocusCheck(fn)
        else:
            keys, fn, _ = row
        scut = QShortcut(QKeySequence(keys), self.widget, activated=fn)
        #mw.shortcuts.append(scut)
    #prevCuts = cuts

Editor.setupShortcuts = _setupShortcuts

mw.setupKeys = _setupKeys
mw.applyShortcuts = _applyShortcuts
AnkiQt.setupKeys = _setupKeys

applyInverters()
mw.setupKeys()
