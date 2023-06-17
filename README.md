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


Currently running in to 400 errors

Theoretically I can just pass in the data as raw bytes in a frame buffer without storing it...?
