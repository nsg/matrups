# matrups

Matrups (MATRix hangUPS) is a Matrix-Hangouts bridge. It uses [matrix-python-sdk](https://github.com/matrix-org/matrix-python-sdk) and [hangups](https://github.com/tdryer/hangups) to setup the bridge.

The bridge assumes that you use a dedicated Google and Matrix user, then add the user to the appropriate chat rooms. 1-to-1 chats are not supported, even it it would probably work if you used your normal Google account.

## Configuration file

There is an sample config file included, rename it to `config.yml` and update the appropriate configuration options. If you use the client Riot for matrix, you can find the user token at the user settings page (the gear icon in the lower left).

If you use the Riot client, the Matrix room ID can be found on the bottom of the rooms settings page (the gear icon in the top). It's called internal ID, starts with a `!` and ends with the matrix servers URL. The easiest way to find the Google Hangouts room ID:s are to invite the bot with an official client and start matrups. Hangouts and Matrix room ID:s are printed on startup.

## First login

On your first login the token.txt file will be populated with an refresh token from Google. If you intend to run the script on a remote server, that may trigger a security warning from Google. The easiest workaround is to run matrups once on a system where you have logged in to the Google account and copy token.txt over to the server.
