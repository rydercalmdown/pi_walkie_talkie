# Raspberry Pi Walkie Talkies
A global walkie-talkie system for me and my friends using Raspberry Pis.


## Architecture
Both the server and client are in this repository, and can be activated by:

```
make run-server
```

or

```
make run-client
```

It's likely best to run the server on a separate cloud hosting service, though you could do it on the pi, simultaneously running the client, as long as that pi has port forwarding so the other clients on the general web can reach it.

## Notes
Do not use the Visual Studio Code console to test this, it won't work.
