Disclaimer: This was entirely vibe-coded using ChatGPT and Cursor.

This is a simple encrypted notepad. On first launch, it asks you to set a password, then generates a JSON file containing the hash and salt used to encrypt your notes. Keep that file safe (i.e. back it up somewhere in high heaven) - you’ll need it to decrypt your content later. Future logins require the same password.

Notes are stored in a notes folder and are fully encrypted - useless without the JSON and your password (which you’ll need to remember). Of course, I am smart enough to know you'd need to exprot those notes to raw text so there's that feature too.

It supports basic formatting (bold, underline, italics), three heading levels, keyboard shortcuts, and UI scaling.

The idea was simple: a notepad you can launch, enter a password, and immediately access all your encrypted notes - local and secure.

Enjoy.

Shortcut guide:
CTRL+N: new note 
CTRL+S: save active note (app auot saves every 3 seconds btw)
CTRL+Z: undo
