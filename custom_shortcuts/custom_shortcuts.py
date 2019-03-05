#Python 3.7.0
from aqt import mw
from aqt.qt import *
from anki.hooks import runHook,addHook
from aqt.utils import showWarning
from aqt.toolbar import Toolbar
from aqt.editor import Editor,EditorWebView
from aqt.reviewer import Reviewer
from anki.utils import json
from bs4 import BeautifulSoup
import warnings
from . import cs_functions as functions

#Gets config.json as config
config = mw.addonManager.getConfig(__name__)
CS_CONFLICTSTR = "Custom Shortcut Conflicts: \n\n"
#config_scuts initialized after cs_traverseKeys
Qt_functions = {"Qt.Key_Enter":Qt.Key_Enter, 
                "Qt.Key_Return":Qt.Key_Return,
                "Qt.Key_Escape":Qt.Key_Escape,
                "Qt.Key_Space":Qt.Key_Space,
                "Qt.Key_Tab":Qt.Key_Tab,
                "Qt.Key_Backspace":Qt.Key_Backspace,
                "Qt.Key_Delete":Qt.Key_Delete,
                "Qt.Key_Left":Qt.Key_Left,
                "Qt.Key_Down":Qt.Key_Down,
                "Qt.Key_Right":Qt.Key_Right,
                "Qt.Key_Up":Qt.Key_Up,
                "Qt.Key_PageUp":Qt.Key_PageUp,
                "Qt.Key_PageDown":Qt.Key_PageDown,
                "<nop>":""
                }

#There is a weird interaction with QShortcuts wherein if there are 2 (or more)
#QShortcuts mapped to the same key and function and both are enabled,
#the shortcut doesn't work

#Part of this code exploits that by adding QShortcuts mapped to the defaults
#and activating/deactivating them to deactivate/activate default shortcuts

#There isn't an obvious way to get the original QShortcut objects, as
#The addons executes after the setup phase (which creates QShortcut objects)

def cs_traverseKeys(Rep, D):
    ret = {}
    for key in D:
        if isinstance(D[key],dict):
            ret[key] = cs_traverseKeys(Rep,D[key])
        elif D[key] not in Rep:
            ret[key] = D[key]
        else:
            ret[key] = Rep[D[key]]
    return ret

config_scuts = cs_traverseKeys(Qt_functions,config)

#This is the worst code I think I've written for custom-shortcuts
#Since QShortcuts cannot reveal their action (to the best of my knowledge),
#This map reconstructs what each QShortcut is supposed to do from its id
#The ids were found manually and are thus incredibly dubious
id_main_config = {-1: "main debug",
                  -2: "main deckbrowser",
                  -3: "main study",
                  -4: "main add",
                  -5: "main browse",
                  -6: "main stats",
                  -7: "main sync"
                  }

#Finds all the shortcuts, figures out relevant ones from hardcoded id check,
#and sets it to the right one
#This function has a side effect of changing the shortcut's id
def cs_main_setupShortcuts():
    qshortcuts = mw.findChildren(QShortcut)
    for scut in qshortcuts:
        if scut.id() in id_main_config:
            scut.setKey(config_scuts[id_main_config[scut.id()]])


#Governs the shortcuts on the main toolbar
def cs_mt_setupShortcuts():
    m = mw.form
    #Goes through and includes anything on the duplicates list
    scuts_list = {
        "m_toolbox quit": [config_scuts["m_toolbox quit"]],
        "m_toolbox preferences": [config_scuts["m_toolbox preferences"]],
        "m_toolbox undo": [config_scuts["m_toolbox undo"]],
        "m_toolbox see documentation": [config_scuts["m_toolbox see documentation"]],
        "m_toolbox switch profile": [config_scuts["m_toolbox switch profile"]],
        "m_toolbox export": [config_scuts["m_toolbox export"]],
        "m_toolbox import": [config_scuts["m_toolbox import"]],
        "m_toolbox study": [config_scuts["m_toolbox study"]],
        "m_toolbox create filtered deck": [config_scuts["m_toolbox create filtered deck"]],
        "m_toolbox addons": [config_scuts["m_toolbox addons"]]
    }
    for act,key in config_scuts["m_toolbox _duplicates"].items():
        scuts_list[act].append(key)
    m.actionExit.setShortcuts(scuts_list["m_toolbox quit"])
    m.actionPreferences.setShortcuts(scuts_list["m_toolbox preferences"])
    m.actionUndo.setShortcuts(scuts_list["m_toolbox undo"])
    m.actionDocumentation.setShortcuts(scuts_list["m_toolbox see documentation"])
    m.actionSwitchProfile.setShortcuts(scuts_list["m_toolbox switch profile"])
    m.actionExport.setShortcuts(scuts_list["m_toolbox export"])
    m.actionImport.setShortcuts(scuts_list["m_toolbox import"])
    m.actionStudyDeck.setShortcuts(scuts_list["m_toolbox study"])
    m.actionCreateFiltered.setShortcuts(scuts_list["m_toolbox create filtered deck"])
    m.actionAdd_ons.setShortcuts(scuts_list["m_toolbox addons"])

#Governs the shortcuts on the review window
def cs_review_setupShortcuts(self):
    dupes = []
    ret = [
        (config_scuts["reviewer edit current"], self.mw.onEditCurrent),
        (config_scuts["reviewer flip card 1"], self.onEnterKey),
        (config_scuts["reviewer flip card 2"], self.onEnterKey),
        (config_scuts["reviewer flip card 3"], self.onEnterKey),
        (config_scuts["reviewer replay audio 1"], self.replayAudio),
        (config_scuts["reviewer replay audio 2"], self.replayAudio),
        (config_scuts["reviewer set flag 1"], lambda: self.setFlag(1)),
        (config_scuts["reviewer set flag 2"], lambda: self.setFlag(2)),
        (config_scuts["reviewer set flag 3"], lambda: self.setFlag(3)),
        (config_scuts["reviewer set flag 4"], lambda: self.setFlag(4)),
        (config_scuts["reviewer set flag 0"], lambda: self.setFlag(0)),
        (config_scuts["reviewer mark card"], self.onMark),
        (config_scuts["reviewer bury note"], self.onBuryNote),
        (config_scuts["reviewer bury card"], self.onBuryCard),
        (config_scuts["reviewer suspend note"], self.onSuspend),
        (config_scuts["reviewer suspend card"], self.onSuspendCard),
        (config_scuts["reviewer delete note"], self.onDelete),
        (config_scuts["reviewer play recorded voice"], self.onReplayRecorded),
        (config_scuts["reviewer record voice"], self.onRecordVoice),
        (config_scuts["reviewer options menu"], self.onOptions),
        (config_scuts["reviewer choice 1"], lambda: self._answerCard(1)),
        (config_scuts["reviewer choice 2"], lambda: self._answerCard(2)),
        (config_scuts["reviewer choice 3"], lambda: self._answerCard(3)),
        (config_scuts["reviewer choice 4"], lambda: self._answerCard(4)),
    ]
    for scut in config_scuts["reviewer _duplicates"]:
        dupes.append((config_scuts["reviewer _duplicates"][scut],self.sToF(scut)))
    return dupes + ret

#The function to setup shortcuts on the Editor
#Something funky is going on with the default MathJax and LaTeX shortcuts
#It does not affect the function (as I currently know of)
def cs_editor_setupShortcuts(self):
    # if a third element is provided, enable shortcut even when no field selected
    cuts = [
        (config_scuts["editor card layout"], self.onCardLayout, True),
        (config_scuts["editor bold"], self.toggleBold),
        (config_scuts["editor italic"], self.toggleItalic),
        (config_scuts["editor underline"], self.toggleUnderline),
        (config_scuts["editor superscript"], self.toggleSuper),
        (config_scuts["editor subscript"], self.toggleSub),
        (config_scuts["editor remove format"], self.removeFormat),
        (config_scuts["editor foreground"], self.onForeground),
        (config_scuts["editor change col"], self.onChangeCol),
        (config_scuts["editor cloze"], self.onCloze),
        (config_scuts["editor cloze alt"], self.onAltCloze),
        (config_scuts["editor add media"], self.onAddMedia),
        (config_scuts["editor record sound"], self.onRecSound),
        (config_scuts["editor insert latex"], self.insertLatex),
        (config_scuts["editor insert latex equation"], self.insertLatexEqn),
        (config_scuts["editor insert latex math environment"], self.insertLatexMathEnv),
        (config_scuts["editor insert mathjax inline"], self.insertMathjaxInline),
        (config_scuts["editor insert mathjax block"], self.insertMathjaxBlock),
        (config_scuts["editor insert mathjax chemistry"], self.insertMathjaxChemistry),
        (config_scuts["editor html edit"], self.onHtmlEdit),
        (config_scuts["editor focus tags"], self.onFocusTags, True),
        (config_scuts["editor _extras"]["paste custom text"], self.customPaste)
    ]
    runHook("setupEditorShortcuts", cuts, self)
    for row in cuts:
        if len(row) == 2:
            keys, fn = row
            fn = self._addFocusCheck(fn)
        else:
            keys, fn, _ = row
        scut = QShortcut(QKeySequence(keys), self.widget, activated=fn)

#IMPLEMENTS Browser shortcuts
def cs_browser_setupShortcuts(self):
    f = self.form
    f.previewButton.setShortcut(config_scuts["window_browser preview"])
    f.actionReschedule.setShortcut(config_scuts["window_browser reschedule"])
    f.actionSelectAll.setShortcut(config_scuts["window_browser select all"])
    f.actionUndo.setShortcut(config_scuts["window_browser undo"])
    f.actionInvertSelection.setShortcut(config_scuts["window_browser invert selection"])
    f.actionFind.setShortcut(config_scuts["window_browser find"])
    f.actionNote.setShortcut(config_scuts["window_browser goto note"])
    f.actionNextCard.setShortcut(config_scuts["window_browser goto next note"])
    f.actionPreviousCard.setShortcut(config_scuts["window_browser goto previous note"])
    f.actionChangeModel.setShortcut(config_scuts["window_browser change note type"])
    f.actionGuide.setShortcut(config_scuts["window_browser guide"])
    f.actionFindReplace.setShortcut(config_scuts["window_browser find and replace"])
    f.actionTags.setShortcut(config_scuts["window_browser filter"])
    f.actionCardList.setShortcut(config_scuts["window_browser goto card list"])
    f.actionReposition.setShortcut(config_scuts["window_browser reposition"])
    f.actionFirstCard.setShortcut(config_scuts["window_browser first card"])
    f.actionLastCard.setShortcut(config_scuts["window_browser last card"])
    f.actionClose.setShortcut(config_scuts["window_browser close"])
    f.action_Info.setShortcut(config_scuts["window_browser info"])
    f.actionAdd_Tags.setShortcut(config_scuts["window_browser add tag"])
    f.actionRemove_Tags.setShortcut(config_scuts["window_browser remove tag"])
    f.actionToggle_Suspend.setShortcut(config_scuts["window_browser suspend"])
    f.actionDelete.setShortcut(config_scuts["window_browser delete"])
    f.actionAdd.setShortcut(config_scuts["window_browser add note"])
    f.actionChange_Deck.setShortcut(config_scuts["window_browser change deck"])
    f.actionRed_Flag.setShortcut(config_scuts["window_browser flag_red"])
    try:
        f.actionOrange_Flag.setShortcut(config_scuts["window_browser flag_orange"])
    except AttributeError:
        f.actionPurple_Flag.setShortcut(config_scuts["window_browser flag_orange"])
    f.actionGreen_Flag.setShortcut(config_scuts["window_browser flag_green"])
    f.actionBlue_Flag.setShortcut(config_scuts["window_browser flag_blue"])
    f.actionSidebar.setShortcut(config_scuts["window_browser goto sidebar"])
    f.actionToggle_Mark.setShortcut(config_scuts["window_browser toggle mark"])
    f.actionClear_Unused_Tags.setShortcut(config_scuts["window_browser clear unused tags"])
    f.actionFindDuplicates.setShortcut(config_scuts["window_browser find duplicates"])
    f.actionSelectNotes.setShortcut(config_scuts["window_browser select notes"])
    f.actionManage_Note_Types.setShortcut(config_scuts["window_browser manage note types"])




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
                    ext_list[sub][key + " in " + e] = val[key].upper()
            else:
                ext_list[sub][e] = val.upper()
        elif sub != "Ω":
            ext_list[sub] = {e:val.upper()}
    inv = {}
    conflictStr = CS_CONFLICTSTR
    conflict = False
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
            if not k:
                continue
            conflict = True
            conflictStr += ", ".join(inv[k])
            conflictStr += "\nshare '" + k + "' as a shortcut\n\n"
    if conflict:
        conflictStr += "\nThese shortcuts will not work.\n"
        conflictStr += "Please change them in the config.json."
        showWarning(conflictStr)

def cs_toolbarCenterLinks(self):
    links = [
            ["decks", _("Decks"), _("Shortcut key: %s") % config_scuts["main deckbrowser"]],
            ["add", _("Add"), _("Shortcut key: %s") % config_scuts["main add"]],
            ["browse", _("Browse"), _("Shortcut key: %s") % config_scuts["main browse"]],
            ["stats", _("Stats"), _("Shortcut key: %s") % config_scuts["main stats"]],
            ["sync", _("Sync"), _("Shortcut key: %s") % config_scuts["main sync"]],
        ]
    return self._linkHTML(links)



#Functions that execute on startup
Editor.customPaste = functions.cs_editor_custom_paste
Editor._customPaste = functions.cs_uEditor_custom_paste
Editor.onAltCloze = functions.cs_editor_onAltCloze
Editor._onAltCloze = functions.cs_uEditor_onAltCloze
Reviewer.sToF = functions.review_sToF
Editor.setupShortcuts = cs_editor_setupShortcuts
Reviewer._shortcutKeys = cs_review_setupShortcuts
Toolbar._centerLinks = cs_toolbarCenterLinks


#Shortcut setup for main window & other startup functions
cs_mt_setupShortcuts()
cs_main_setupShortcuts()
cs_conflictDetect()

#Redraws the toolbar with the new shortcuts
mw.toolbar.draw()

#Hooks to setup shortcuts at the right time
addHook('browser.setupMenus', cs_browser_setupShortcuts)
