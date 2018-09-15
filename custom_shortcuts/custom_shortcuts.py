#Python 3.7.0
from aqt.main import AnkiQt
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook, runHook
from aqt.utils import showWarning
from aqt.toolbar import Toolbar
from aqt.editor import Editor
from aqt.reviewer import Reviewer


#TODO: Change the toolbar & editor toolbar to reflect changed keys

#Gets config.json as config
config = mw.addonManager.getConfig(__name__)
CS_CONFLICTSTR = "Custom Shortcut Conflicts: \n\n"


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
#Unsure if this is possible
def _applyShortcuts(shortcuts):
    qshortcuts = []
    for key, fn in shortcuts:
        if key not in mw.inversionSet:
            scut = QShortcut(QKeySequence(key), mw, activated=fn)
            scut.setAutoRepeat(False)
            qshortcuts.append(scut)
        else:
            mw.inverters[mw.inversionSet.index(key)].setEnabled(False)
    return qshortcuts

#Initialize custom keys
def cs_initKeys():
    cuts = [
        config["main debug"],
        config["main deckbrowser"],
        config["main study"],
        config["main add"],
        config["main browse"],
        config["main stats"],
        config["main sync"]
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

#Governs the shortcuts on the main toolbar
def cs_mtShortcuts():
    m = mw.form
    m.actionExit.setShortcut(config["m_toolbox quit"])
    m.actionPreferences.setShortcut(config["m_toolbox preferences"])
    m.actionUndo.setShortcut(config["m_toolbox undo"])
    m.actionDocumentation.setShortcut(config["m_toolbox see documentation"])
    m.actionSwitchProfile.setShortcut(config["m_toolbox switch profile"])
    m.actionExport.setShortcut(config["m_toolbox export"])
    m.actionImport.setShortcut(config["m_toolbox import"])
    m.actionStudyDeck.setShortcut(config["m_toolbox study"])
    m.actionCreateFiltered.setShortcut(config["m_toolbox create filtered deck"])
    m.actionAdd_ons.setShortcut(config["m_toolbox addons"])

#Converts json shortcuts into functions for the reviewer
#sToF: shortcutToFunction
def review_sToF(self,scut):

    #"reviewer" is retained for copy-pastability, may be removed later
    sdict = {
        "reviewer edit current": self.onEditCurrent,
        "reviewer flip card": self.onEnterKey,
        "reviewer flip card 1": self.onEnterKey,
        "reviewer flip card 2": self.onEnterKey,
        "reviewer flip card 3": self.onEnterKey,
        "reviewer options menu": self.onOptions,
        "reviewer record voice": self.onRecordVoice,
        "reviewer play recorded voice": self.onReplayRecorded,
        "reviewer play recorded voice 1": self.onReplayRecorded,
        "reviewer play recorded voice 2": self.onReplayRecorded,
        "reviewer delete note": self.onDelete,
        "reviewer suspend card": self.onSuspendCard,
        "reviewer suspend note": self.onSuspend,
        "reviewer bury card": self.onBuryCard,
        "reviewer bury note": self.onBuryNote,
        "reviewer mark card": self.onMark,
        "reviewer set flag 1": lambda: self.setFlag(1),
        "reviewer set flag 2": lambda: self.setFlag(2),
        "reviewer set flag 3": lambda: self.setFlag(3),
        "reviewer set flag 4": lambda: self.setFlag(4),
        "reviewer set flag 0": lambda: self.setFlag(0),
        "reviewer replay audio": self.replayAudio,
        "reviewer choice 1": lambda: self._answerCard(1),
        "reviewer choice 2": lambda: self._answerCard(2),
        "reviewer choice 3": lambda: self._answerCard(3),
        "reviewer choice 4": lambda: self._answerCard(4),
    }
    return sdict[scut]

#Governs the shortcuts on the review window
def review_shortcutKeys(self):
    dupes = []
    for scut in config["reviewer _duplicates"]:
        dupes.append((config["reviewer _duplicates"][scut],self.sToF(scut)))
    ret = [
    (config["reviewer edit current"], self.onEditCurrent),
    (config["reviewer flip card 1"], self.onEnterKey),
    (config["reviewer flip card 2"], self.onEnterKey),
    (config["reviewer flip card 3"], self.onEnterKey),
    (config["reviewer replay audio 1"], self.replayAudio),
    (config["reviewer replay audio 2"], self.replayAudio),
    (config["reviewer set flag 1"], lambda: self.setFlag(1)),
    (config["reviewer set flag 2"], lambda: self.setFlag(2)),
    (config["reviewer set flag 3"], lambda: self.setFlag(3)),
    (config["reviewer set flag 4"], lambda: self.setFlag(4)),
    (config["reviewer set flag 0"], lambda: self.setFlag(0)),
    (config["reviewer mark card"], self.onMark),
    (config["reviewer bury note"], self.onBuryNote),
    (config["reviewer bury card"], self.onBuryCard),
    (config["reviewer suspend note"], self.onSuspend),
    (config["reviewer suspend card"], self.onSuspendCard),
    (config["reviewer delete note"], self.onDelete),
    (config["reviewer play recorded voice"], self.onReplayRecorded),
    (config["reviewer record voice"], self.onRecordVoice),
    (config["reviewer options menu"], self.onOptions),
    (config["reviewer choice 1"], lambda: self._answerCard(1)),
    (config["reviewer choice 2"], lambda: self._answerCard(2)),
    (config["reviewer choice 3"], lambda: self._answerCard(3)),
    (config["reviewer choice 4"], lambda: self._answerCard(4)),
    ]
    return dupes + ret

def _setupShortcuts(self):
    # if a third element is provided, enable shortcut even when no field selected
    cuts = [
        (config["editor card layout"], self.onCardLayout, True),
        (config["editor bold"], self.toggleBold),
        (config["editor italic"], self.toggleItalic),
        (config["editor underline"], self.toggleUnderline),
        (config["editor superscript"], self.toggleSuper),
        (config["editor subscript"], self.toggleSub),
        (config["editor remove format"], self.removeFormat),
        (config["editor foreground"], self.onForeground),
        (config["editor change col"], self.onChangeCol),
        (config["editor cloze"], self.onCloze),
        (config["editor cloze alt"], self.onCloze),
        (config["editor add media"], self.onAddMedia),
        (config["editor record sound"], self.onRecSound),
        (config["editor insert latex"], self.insertLatex),
        (config["editor insert latex equation"], self.insertLatexEqn),
        (config["editor insert latex math environment"], self.insertLatexMathEnv),
        (config["editor insert mathjax inline"], self.insertMathjaxInline),
        (config["editor insert mathjax block"], self.insertMathjaxBlock),
        (config["editor insert mathjax chemistry"], self.insertMathjaxChemistry),
        (config["editor html edit"], self.onHtmlEdit),
        (config["editor focus tags"], self.onFocusTags, True)
    ]
    runHook("setupEditorShortcuts", cuts, self)
    for row in cuts:
        if len(row) == 2:
            keys, fn = row
            fn = self._addFocusCheck(fn)
        else:
            keys, fn, _ = row
        scut = QShortcut(QKeySequence(keys), self.widget, activated=fn)

#detects shortcut conflicts
#Ignores the Add-on (Ω) options
def cs_conflictDetect():
    if config["Ω enable conflict warning"].upper() != "Y":
        return
    ext_list = {}
    dupes = False
    for e in config:
        sub = e[0:(e.find(" "))]
        val = config[e]
        if sub in ext_list:
            if isinstance(val,dict):
                for key in val:
                    ext_list[sub][key + " in _duplicates"] = val[key].upper()
            else:
                ext_list[sub][e] = val.upper()
        elif sub != "Ω":
            ext_list[sub] = {e:val.upper()}
    inv = {}
    conflictStr = CS_CONFLICTSTR
    for key in ext_list:
        inv = {}
        x = ext_list[key]
        for e in x:
            if x[e] not in inv:
                inv[x[e]] = [e]
            else:
                inv[x[e]].append(e)
        for k in inv:
            if(len(inv[k])) == 1:
                continue
            if k == "<NOP>":
                continue
            conflictStr += ", ".join(inv[k])
            conflictStr += "\nshare '" + k + "' as a shortcut\n\n"

    if(len(conflictStr) != len(CS_CONFLICTSTR)):
        conflictStr += "\nThese shortcuts will not work.\n"
        conflictStr += "Please change them in the config.json."
        showWarning(conflictStr)


Editor.setupShortcuts = _setupShortcuts
Reviewer._shortcutKeys = review_shortcutKeys
Reviewer.sToF = review_sToF

mw.applyShortcuts = _applyShortcuts

cs_applyInverters()
cs_initKeys()
cs_mtShortcuts()
cs_conflictDetect()
