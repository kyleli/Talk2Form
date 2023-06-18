# GPT Based Voice to Form Filler

Currently tested against medical applications, but adaptable to other usecases.
Watch how to use this here:
https://youtu.be/3pcRthql4OU

Todo:
Frontend
- Need to scroll earlier since the bottom UI blocks the items.
- No way to currently delete forms or questions

Backend Database
- Connect User Accounts with Dashboard Content, Forms, Audio Recordings, and Form Contents

Others:
- Add Night Mode to Site
- Reconfigure UI for proper screens
- Rebuild the UI to have a grid panel system

Issues:
- Need to warn users that deleting template will delete all associated forms.
- No way to delete user account
- No way to change username
- No way to recover your password if you forget it (L)
- No 2FA
- Many fail cases e.g. what happens if user records audio twice or hit GPT API limit.

Currently the system requires the user to click the bottom right button, which then leads to another screen.
This screen should be where the user records audio and then processes the questions against the audio file and autofills the data and then displays it to the user.
This is what it needs to do.

Need to now link a new audio thing with the new form. The audio button should call the new audio thing to start recording.
The user needs to be able to click record to re-record on the form if needed but right now we're implementing.
