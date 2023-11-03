## Dejure Bot
### Configure

```json
{
    "debug": true, // Enable debug log level
    "bot" : {
        "token": "" //  Must set env var BOT_TOKEN
    },
    // Set admins ID from telegram ID
    "admins": [
        0
    ],
    "database": {
        "mode": "dev" // Database in memory
    }
}
```
```bash
cp config-default.json config.json

```