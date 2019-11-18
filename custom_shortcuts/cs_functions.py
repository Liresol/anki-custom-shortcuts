import re
import anki
from aqt.utils import tooltip,showInfo
from aqt.qt import *
from aqt import mw

def get_version():
    """Return the integer subversion of Anki on which the addon is run ("2.1.11" -> 11)"""
    return int(anki.version.split('.')[2])

def cs_editor_onAltCloze(self):
    self.saveNow(self._onAltCloze, keepFocus=True)

def cs_uEditor_onAltCloze(self):
        # check that the model is set up for cloze deletion
    if not re.search('{{(.*:)*cloze:',self.note.model()['tmpls'][0]['qfmt']):
        if self.addMode:
            tooltip(_("Warning, cloze deletions will not work until "
                "you switch the type at the top to Cloze."))
        else:
            showInfo(_("""\
To make a cloze deletion on an existing note, you need to change it \
to a cloze type first, via Edit>Change Note Type."""))
            return
        # find the highest existing cloze
    highest = 0
    for name, val in list(self.note.items()):
        m = re.findall(r"\{\{c(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
        # reuse last?
    highest = max(1, highest)
    self.web.eval("wrap('{{c%d::', '}}');" % highest)

#Converts json shortcuts into functions for the reviewer
#sToF: shortcutToFunction
def review_sToF(self,scut):

    #"reviewer" is retained for copy-pastability, may be removed later
    #"self.mw.onEditCurrent" is exactly how it was in reviewer.py, DO NOT CHANGE
    sdict = {
        "reviewer edit current": self.mw.onEditCurrent,
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

