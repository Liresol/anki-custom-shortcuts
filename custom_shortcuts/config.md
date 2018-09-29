###To disable a shortcut, set that shortcut to `<nop>`


##Editor Options

"editor add media": Add external media

"editor bold": Toggle bold 

"editor card layout": Change Card Layout

"editor change col": Change text color

"editor cloze":Insert Anki cloze

"editor cloze alt": Same as above

"editor focus tags": Switch focus to the Tags field

"editor foreground": Set foreground color

"editor html edit": Edit the card's HTML

"editor insert latex": Insert LaTeX formatted text

"editor insert latex equation": Insert a LaTeX equation

"editor insert latex math environment": Insert a LaTeX math environment

"editor insert mathjax block": Insert a MathJax block

"editor insert mathjax chemistry": Insert a chemistry thing in MathJax

"editor insert mathjax inline": Insert an inline MathJax expresesion

"editor italic": Toggle italics

"editor record sound": Record sound

"editor remove format": Remove card formatting

"editor subscript": Toggle subscript

"editor superscript": Toggle superscript

"editor underline": Toggle underline

"editor \_extras": Special shortcuts with functionality not originally in Anki. Default mapped to `<nop>` (no shortcut).

**In the future, these shortcuts may be removed and put into a new add-on, as they are not part of Anki's default functionality.**

Within "editor \_extras":

"paste custom text": Pastes a custom piece of html text into a card field (defined in "\u03a9 custom paste text")

##Main Toolbox Options

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

"main add": Add new card

"main browse": Enter card browser

"main debug": Open debug screen

"main deckbrowser": Go back to home screen

"main stats": Enter stats screen

"main study": Study current deck

"main sync": Synchronize with AnkiWeb

##Reviewer Options

"reviewer bury card": Bury this card

"reviewer bury note": Bury this note (card and associated cards)

"reviewer choice [1234]": Select 1/2/3/4 (Again/Hard/Good/Easy or Again/Good/Easy)

"reviewer delete note": Delete this note

"reviewer edit current": Edit the card currently being reviewed

"reviewer flip card [123]": Flip the card to see the answer

"reviewer mark card": Mark this card with a star

"reviewer options menu": Go to the review options menu

"reviewer play recorded voice": If there is a recorded voice, play it

"reviewer record voice": Record your voice

"reviewer replay audio [12]": Replay audio attached to the card

"reviewer set flag [12340]": Set a flag on this card (or none for 0), changing colors depending on the number (1/2/3/4)

"reviewer suspend card": Suspend this card

"reviewer suspend note": Suspend this note

"reviewer \_duplicates": Takes functions and binds them to new shortcuts.

This object takes inputs of the form "(function keyword)":"(shortcut)", separated by commas. (e.g. {"reviewer mark card":"]","reviewer flip card 1":"-"})

All the keywords are exactly the same as the keywords used in the json file, making the lines copy-pastable. (Those who want to remove the numbers from stuff like "reviewer flip card" can do so as well)

**Make sure to remap keys to empty keyspace.**

##Add-on Preferences

**These options are for changing a few settings on the add-on itself.**

"\u03a9 custom paste end style": For the exceptionally lazy (like me). If set to "y", inserts a `</span>` and a zero-width space at the end of the custom text to stop the custom style from bleeding into new text.

Otherwise, the custom paste will behave exactly like regular paste.

"\u03a9 custom paste text": Controls what html will be pasted by "custom paste" in "editor \_extras"	
e.g. `"\u03a9 custom paste text": "<span style=\"font-size: 20px; color:#3399ff\">◆</span>"`

"\u03a9 enable conflict warning": If set to "y", shows a warning window whenever two shortcuts of the same type are set to the same key.

