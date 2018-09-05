###To disable a shortcut, set that shortcut to `<nop>` or another invalid shortcut.

##Home Options

**NOTE: Setting these to "Ctrl+:", "d", "s", "a", "b", "t", or "y" will not work if they are not the default setting for that function.**

"debug": Open debug screen

"deckbrowser": Go back to home screen

"study": Study current deck

"add": Add new card

"browse": Enter card browser

"stats": Enter stats screen

"sync": Syncronize with AnkiWeb

##Editor Options

"card layout": Change Card Layout

"bold": Toggle bold 

"italic": Toggle italics

"underline": Toggle underline

"superscript": Toggle superscript

"subscript": Toggle subscript

"remove format": Remove card formatting

"foreground": Set foreground color

"change col": Change text color

"cloze":Insert Anki cloze

"cloze alt": Same as above

"add media": Add external media

"record sound": Record sound

"insert latex": Insert LaTeX formatted text

"insert latex equation": Insert a LaTeX equation

"insert latex math environment": Insert a LaTeX math environment

"insert mathjax inline": Insert an inline MathJax expresesion

"insert mathjax block": Insert a MathJax block

"insert mathjax chemistry": Insert a chemistry thing in MathJax

"html edit": Edit the card's HTML

"focus tags": Switch focus to the Tags field

##Reviewer Options

"edit current": Edit the card currently being reviewed

"flip card [123]": Flip the card to see the answer

"replay audio [12]": Replay audio attached to the card

"set flag [12340]": Set a flag on this card (or none for 0), changing colors depending on the number (1/2/3/4)

"mark card": Mark this card with a star

"bury note": Bury this note (card and associated cards)

"bury card": Bury this card

"suspend note": Suspend this note

"suspend card": Suspend this card

"delete note": Delete this note

"play recorded voice": If there is a recorded voice, play it

"record voice": Record your voice

"options menu": Go to the review options menu

"choice [1234]": Select 1/2/3/4 (Again/Hard/Good/Easy or Again/Good/Easy)

"_duplicates": Takes functions and binds them to new shortcuts.

This object takes inputs of the form "(function keyword)":"(shortcut)", separated by commas. (e.g. {"reviewer mark card":"]","reviewer flip card 1":"-"})

All the keywords are exactly the same as the keywords used in the json file, making the lines copy-pastable. (Those who want to remove the numbers from stuff like "reviewer flip card" can do so as well)

**Make sure to remap keys to empty keyspace.**

##Main Toolbox Options
**NOTE: These options are prefixed with "m_toolbox".**

"m_toolbox quit": Quit Anki

"m_toolbox preferences": Go to the user preferences window

"m_toolbox undo": Undo the last actio

"m_toolbox see documentation": Go to the Anki manual

"m_toolbox switch profile": Switch user profiles

"m_toolbox export": Export the user's decks

"m_toolbox import": Import a deck file (.apkg, etc.)

"m_toolbox study": Start studying the selected deck

"m_toolbox create filtered deck": Create a filtered deck

"m_toolbox addons": Go to the addons window

}

