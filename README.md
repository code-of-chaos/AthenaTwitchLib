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
  - Other older versions of Python are not currently supported. 
  - These older versions will probably not be supported by [@AndreasSas](https://github.com/AndreasSas) himself, but if you want to contribute to the project and make this package compatible with older versions of Python, Pull requests are always welcome.

---
## Quick Example
The following example is a working bot, but currently only meant as proof of work as the package is still in its early stages of being developed and needs some heavy tuning.

Stay tuned for updates while we work on this on [stream](https://www.twitch.tv/directiveathena) or come hang out in the [discord](https://discord.com/invite/6JcDbhXkCH).

```python
# --- Imports ---
import AthenaTwitchBot  # Main import for the bot to work
import AthenaColor      # Not needed for the following example, but is a dependency
import AthenaLib        # Not needed for the following example, but is a dependency

# --- Twitch bot ---
class newBot(AthenaTwitchBot.TwitchBot):
  def __init__(self):
    super(newBot, self).__init__(
      # Make sure you fill in the fields below
      #   else the bot will not be able to be authenticated by Twitch
      nickname="...",       # <--- The registered bot name
      oauth_token="...",    # <--- the registered bots access token. Don't put this in plain text!
      channel="...",        # <--- The twitch channel name you want to bind your bot to
      prefix="!",           # <--- The "default" prefix is an exclamation point, but technically you can assign any string as a prefix 
    )

  # - Command -
  #   A command is only ran when it is invoked by a user in chat
  #   In the following case this would be by typing "!ping" in chat
  @AthenaTwitchBot.command_method(name="ping")
  def command_ping(self, context: AthenaTwitchBot.TwitchMessageContext):
    context.reply("pong!")  # a "context.reply" function will reply to the user whi invoked the command

  # - Task -
  #   A task is run automatically every "delay" amount of seconds
  #   In the following case, the method will be run every minute
  #   The "wait_before" kwarg defines if the asyncio.sleep runs before or after the first call of the callback
  @AthenaTwitchBot.scheduled_task_method(delay=60, wait_before=True)
  def task_post_github(self, context: AthenaTwitchBot.TwitchMessageContext):
    context.write(f"This bot is made possible by: https://github.com/DirectiveAthena/AthenaTwitchBot")

# --- Main function ---
def main():
  AthenaTwitchBot.launch(
    bot=newBot(),
    ssl=True  # set to true to enable ssl connection to Twitch
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