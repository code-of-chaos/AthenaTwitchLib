# - AthenaTwitchBot -
[![pypi](https://img.shields.io/pypi/v/AthenaTwitchBot)](https://pypi.org/project/AthenaTwitchBot/) [![GitHub license](https://img.shields.io/github/license/DirectiveAthena/AthenaTwitchBot)](https://github.com/DirectiveAthena/VerSC-AthenaColor/blob/master/LICENSE) [![Discord](https://img.shields.io/discord/814599159926620160?color=maroon)](https://discord.gg/6JcDbhXkCH) [![Downloads](https://pepy.tech/badge/athenatwitchbot)](https://pepy.tech/project/athenatwitchbot)

--- 
## Package Details
#### Details and features 
- A library to connect to the Twitch IRC system for a chatbot to utilize 
- Isn't dependent on 3rd party packages, except for those that have been created by [@AndreasSas](https://github.com/AndreasSas)
  - These can be designated by the leading "*Athena*..."
  - These packages aren't seen as a 3rd party dependency as they are all made by the "same party"

#### Python Version
- Supported Python versions: **3.10**
  - Other older versions of Python are not gonna be supported. 

---
## Quick Example
The following example is a working bot, but currently only meant as proof of work as the package is still in its early stages of being developed and needs some heavy tuning.

Stay tuned for updates while we work on this on [stream](https://www.twitch.tv/directiveathena) or come hang out in the [discord](https://discord.com/invite/6JcDbhXkCH).

```python
# --- Imports ---
import os

from AthenaTwitchLib.models.twitch_bot.twitch_bot import TwitchBot
from AthenaTwitchLib.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchLib.models.twitch_bot.message_context import MessageContext
from AthenaTwitchLib.models.launcher import Launcher
from AthenaTwitchLib.models.twitch_channel import TwitchChannel

# --- Code ---
class SomeBot(TwitchBot):
    def __init__(self):
        super(SomeBot, self).__init__(
            nickname=..., # <--- your bot name
            oauth_token=os.getenv("TWITCH_TOKEN"),
            channel=TwitchChannel(...), # <--- your channel name
            command_prefix="!",
            client_id=os.getenv("TWITCH_CLIENT_ID")
        )

    @BotCommand.register(name="today")
    async def command_today(self, context: MessageContext):
        context.reply(f"Today we will be working on: ..." )

# -----------------------------------------------------------------------------
def main():
    Launcher.start_Bot(
        bot=SomeBot(),
        sll=True,
    )

if __name__ == '__main__':
    main()

```

---
## Documentation
Full documentation can be found at:
**[directiveathena.com/docu](https://publish.obsidian.md/directiveathena/)** (redirect to Obsidian.md publish site)
(Reminder, the documentation is still under heavy development)

---
## Install
To install the package in your Python environment

```
pip install AthenaTwitchBot --upgrade
```

---

## Links 
Project files can be found at:    
- [GitHub Repo](https://github.com/DirectiveAthena/AthenaTwitchBot)     
- [Pypi link](https://pypi.org/project/AthenaTwitchBot/)    

---

## Disclaimer
With  *No Dependency*, the standard library is not counted as a dependency

---
Made By Andreas Sas,` 2022`
