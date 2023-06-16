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

Currently the system requires the user to click the bottom right button, which then leads to another screen.
This screen should be where the user records audio and then processes the questions against the audio file and autofills the data and then displays it to the user.
This is what it needs to do.


Need to now link a new audio thing with the new form. The audio button should call the new audio thing to start recording.
The user needs to be able to click record to re-record on the form if needed but right now we're implementing.

Look into server side events or websockets (Ideally Websocket)
- Push from server into the site
- Pulling is easier to implement but loops
