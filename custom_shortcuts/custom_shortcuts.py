#Last updated to be useful for: Anki 2.1.21
from anki.lang import _
from aqt import mw
from aqt.qt import *
from anki.hooks import runHook,addHook
from anki.lang import _
from aqt.utils import showWarning
from aqt.toolbar import Toolbar
from aqt.editor import Editor,EditorWebView
from aqt.reviewer import Reviewer
from aqt.browser import Browser
from anki.utils import json
from bs4 import BeautifulSoup
import warnings
from . import cs_functions as functions

#Anki before version 2.1.20 does not use aqt.gui_hooks
try:
    from aqt import gui_hooks
    new_hooks = True
except:
    new_hooks = False

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
        elif D[key] in Rep:
            ret[key] = Rep[D[key]]
        else:
            ret[key] = D[key]
    return ret

#This contains the processed shortcuts used for the rest of the functions
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
    if functions.get_version() >= 20:
        ret += [
            (config_scuts["reviewer pause audio"], self.on_pause_audio),
            (config_scuts["reviewer seek backward"], self.on_seek_backward),
            (config_scuts["reviewer seek forward"], self.on_seek_forward),
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
        (config_scuts["editor html edit"], self.onHtmlEdit),
        (config_scuts["editor focus tags"], self.onFocusTags, True),
        (config_scuts["editor _extras"]["paste custom text"],
         lambda text=config_scuts["Ω custom paste text"]: self.customPaste(text))
    ]
    for label in config_scuts["editor _pastes"]:
        if label in config_scuts["Ω custom paste extra texts"]:
            scut = config_scuts["editor _pastes"][label]
            temp = config_scuts["Ω custom paste extra texts"][label]
            cuts.append((scut, lambda text=temp: self.customPaste(text)))
    #There is a try-except clause to handle 2.1.0 version, which does not have this shortcut
    try:
        cuts.append((config_scuts["editor insert mathjax chemistry"], self.insertMathjaxChemistry))
    except AttributeError:
        pass
    if new_hooks:
        gui_hooks.editor_did_init_shortcuts(cuts, self)
    else:
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

#Mimics the style of other Anki functions, analogue of customPaste
#Note that the saveNow function used earler takes the cursor to the end of the line,
#as it is meant to save work before entering a new window
def cs_editor_custom_paste(self, text):
    self._customPaste(text)

#Mimics the style of other Anki functions, analogue of _customPaste
def cs_uEditor_custom_paste(self, text):
    html = text
    if config_scuts["Ω custom paste end style"].upper() == "Y":
        html += "</span>\u200b"
    with warnings.catch_warnings() as w:
        warnings.simplefilter('ignore', UserWarning)
        html = str(BeautifulSoup(html, "html.parser"))
    self.doPaste(html,True,True)

                        

#detects shortcut conflicts
#Gets all the shortcuts in a given object of the form {name: scut, ...} and names them
#Returns a dictionary of the form {scut: [labels of objects with that scut], ...}
def cs_getAllScuts(obj, strCont):
    res = {}
    for key in obj:
        if isinstance(obj[key], dict):
            rec = cs_getAllScuts(obj[key], key + " in " + strCont)
            for term in rec:
                if term in res:
                    res[term] += rec[term]
                else:
                    res[term] = rec[term]
        else:
            text_scut = obj[key].upper()
            if text_scut in res:
                res[text_scut].append(key + " in " + strCont)
            else:
                res[text_scut] = [key + " in " + strCont]
    return res

#Ignores the Add-on (Ω) options
def cs_conflictDetect():
    if config["Ω enable conflict warning"].upper() != "Y":
        return
    ext_list = {}
    for e in config:
        sub = e[0:(e.find(" "))]
        val = config[e]
        if sub == "Ω":
            continue
        if sub not in ext_list:
            ext_list[sub] = {}
        if isinstance(val, dict):
            scuts = cs_getAllScuts(val, e)
            for scut in scuts:
                if scut in ext_list[sub]:
                    ext_list[sub][scut] += scuts[scut]
                else:
                    ext_list[sub][scut] = scuts[scut]
        else:
            text_val = val.upper()
            if text_val in ext_list:
                ext_list[sub][text_val].append(e)
            else:
                ext_list[sub][text_val] = [e]
    conflictStr = CS_CONFLICTSTR
    conflict = False
    for key in ext_list:
        for k in ext_list[key]:
            if len(ext_list[key][k]) == 1:
                continue
            if k == "<NOP>":
                continue
            if not k:
                continue
            conflict = True
            conflictStr += ", ".join(ext_list[key][k])
            conflictStr += "\nshare '" + k + "' as a shortcut\n\n"
    if conflict:
        conflictStr += "\nThese shortcuts will not work.\n"
        conflictStr += "Please change them in the config.json."
        showWarning(conflictStr)


def cs_toolbarCenterLinks(self):
    try:
        links = [
            self.create_link(
                "decks",
                _("Decks"),
                self._deckLinkHandler,
                tip=_("Shortcut key: %s") % "D",
                id="decks",
            ),
            self.create_link(
                "add",
                _("Add"),
                self._addLinkHandler,
                tip=_("Shortcut key: %s") % "A",
                id="add",
            ),
            self.create_link(
                "browse",
                _("Browse"),
                self._browseLinkHandler,
                tip=_("Shortcut key: %s") % "B",
                id="browse",
            ),
            self.create_link(
                "stats",
                _("Stats"),
                self._statsLinkHandler,
                tip=_("Shortcut key: %s") % "T",
                id="stats",
            ),
        ]

        links.append(self._create_sync_link())

        gui_hooks.top_toolbar_did_init_links(links, self)

        return "\n".join(links)
    except:
        links = [
            ["decks", _("Decks"), _("Shortcut key: %s") % config_scuts["main deckbrowser"]],
            ["add", _("Add"), _("Shortcut key: %s") % config_scuts["main add"]],
            ["browse", _("Browse"), _("Shortcut key: %s") % config_scuts["main browse"]],
            ["stats", _("Stats"), _("Shortcut key: %s") % config_scuts["main stats"]],
            ["sync", _("Sync"), _("Shortcut key: %s") % config_scuts["main sync"]],
            ]
        return self._linkHTML(links)


def cs_browser_basicFilter(self, txt):
    self.form.searchEdit.lineEdit().setText(txt)
    self.onSearchActivated()

#Wtf
#Inserts the custom filter shortcuts upon browser startup
def cs_browser_setupEditor(self):
    self.editor = Editor(self.mw, self.form.fieldsArea, self)
    self.csFilterScuts = {}
    self.csFilterFuncs = {}
    for filt in config_scuts["window_browser _filters"]:
        scut = config_scuts["window_browser _filters"][filt]
        self.csFilterFuncs[filt] = lambda txt=filt: cs_browser_basicFilter(self, txt)
        self.csFilterScuts[filt] = QShortcut(QKeySequence(scut), self)
        self.csFilterScuts[filt].activated.connect(self.csFilterFuncs[filt])
    if config_scuts["window_browser save current filter"]:
        self.csSaveFilterScut = QShortcut(QKeySequence(config_scuts["window_browser save current filter"]), self)
        self.csSaveFilterScut.activated.connect(self._onSaveFilter)
    if config_scuts["window_browser remove current filter"]:
        self.csRemoveFilterScut = QShortcut(QKeySequence(config_scuts["window_browser remove current filter"]), self)
        self.csRemoveFilterScut.activated.connect(self.csRemoveFilterFunc)

#Functions that execute on startup
if config_scuts["Ω enable main"].upper() == 'Y':
    Toolbar._centerLinks = cs_toolbarCenterLinks
    cs_main_setupShortcuts()
if config_scuts["Ω enable editor"].upper() == 'Y':
    Editor.onAltCloze = functions.cs_editor_onAltCloze
    Editor._onAltCloze = functions.cs_uEditor_onAltCloze
    Editor.customPaste = cs_editor_custom_paste
    Editor._customPaste = cs_uEditor_custom_paste
    Editor.setupShortcuts = cs_editor_setupShortcuts
if config_scuts["Ω enable reviewer"].upper() == 'Y':
    Reviewer._shortcutKeys = cs_review_setupShortcuts
    Reviewer.sToF = functions.review_sToF
if config_scuts["Ω enable m_toolbox"].upper() == 'Y':
    cs_mt_setupShortcuts()
#Hooks to setup shortcuts at the right time
if config_scuts["Ω enable window_browser"].upper() == 'Y':
    Browser.csRemoveFilterFunc = functions.remove_filter
    Browser.setupEditor = cs_browser_setupEditor
    addHook('browser.setupMenus', cs_browser_setupShortcuts)

#Detects all conflicts, regardless of enable status
cs_conflictDetect()

#Redraws the toolbar with the new shortcuts
mw.toolbar.draw()
