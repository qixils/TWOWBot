# TWOWBot
Discord bot made to host mini-sized TWOW games.

# Developer Notes
`data.txt` layout:

```md
ulong # channel ID that's setup for mini TWOWs
int # mini TWOW status
int # mini TWOW round number
```

mini twow statuses:
- 0: no game
- 1: game started, waiting for players
- 2: game started, waiting for prompt
- 3: prompt submitted, waiting for players to submit entries
- 4: players submitted, waiting for voting
- 5: quick intermission to display results, go back to 2, increase round number
