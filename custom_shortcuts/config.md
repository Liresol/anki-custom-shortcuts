###To disable a shortcut, set that shortcut to `<nop>`


##Editor Options

"add media": Add external media

"bold": Toggle bold 

"card layout": Change Card Layout

"change col": Change text color

"cloze":Insert Anki cloze

"cloze alt": Same as above

"focus tags": Switch focus to the Tags field

"foreground": Set foreground color

"html edit": Edit the card's HTML

"insert latex": Insert LaTeX formatted text

"insert latex equation": Insert a LaTeX equation

"insert latex math environment": Insert a LaTeX math environment

"insert mathjax block": Insert a MathJax block

"insert mathjax chemistry": Insert a chemistry thing in MathJax

"insert mathjax inline": Insert an inline MathJax expresesion

"italic": Toggle italics

"record sound": Record sound

"remove format": Remove card formatting

"subscript": Toggle subscript

"superscript": Toggle superscript

"underline": Toggle underline

##Main Toolbox Options

**These options are prefixed with "m_toolbox".**

"m_toolbox addons": Go to the addons window

"m_toolbox create filtered deck": Create a filtered deck

"m_toolbox export": Export the user's decks

"m_toolbox import": Import a deck file (.apkg, etc.)

"m_toolbox preferences": Go to the user preferences window

"m_toolbox quit": Quit Anki

"m_toolbox see documentation": Go to the Anki manual

"m_toolbox study": Start studying the selected deck

"m_toolbox switch profile": Switch user profiles

"m_toolbox undo": Undo the last action


##Home Options

**NOTE: Setting these to "Ctrl+:", "d", "s", "a", "b", "t", or "y" will not work if they are not the default setting for that function.**

**These options are prefixed with "main".**

"add": Add new card

"browse": Enter card browser

"debug": Open debug screen

"deckbrowser": Go back to home screen

"stats": Enter stats screen

"study": Study current deck

"sync": Synchronize with AnkiWeb

##Reviewer Options

"bury card": Bury this card

"bury note": Bury this note (card and associated cards)

"choice [1234]": Select 1/2/3/4 (Again/Hard/Good/Easy or Again/Good/Easy)

"delete note": Delete this note

"edit current": Edit the card currently being reviewed

"flip card [123]": Flip the card to see the answer

"mark card": Mark this card with a star

"options menu": Go to the review options menu

"play recorded voice": If there is a recorded voice, play it

"record voice": Record your voice

"replay audio [12]": Replay audio attached to the card

"set flag [12340]": Set a flag on this card (or none for 0), changing colors depending on the number (1/2/3/4)

"suspend card": Suspend this card

"suspend note": Suspend this note

"_duplicates": Takes functions and binds them to new shortcuts.

This object takes inputs of the form "(function keyword)":"(shortcut)", separated by commas. (e.g. {"reviewer mark card":"]","reviewer flip card 1":"-"})

All the keywords are exactly the same as the keywords used in the json file, making the lines copy-pastable. (Those who want to remove the numbers from stuff like "reviewer flip card" can do so as well)

**Make sure to remap keys to empty keyspace.**

##Add-on Preferences

**These options are prefixed with "Ω".**

"Ω enable conflict warning": If set to "y", shows a warning window whenever two shortcuts of the same type are set to the same key.
