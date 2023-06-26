## system management tools
- all tools designed for i3 on arch
- some tools use custom modules from the [modules](https://github.com/mikeredev/modules) repo
- any rofi custom themes are in the [dotfiles](https://github.com/mikeredev/dotfiles/tree/main/rofi/themes) repo

### backup-dotfiles
- check selected files for changes and copy them to another folder
- configured by [backup-dotfiles.json](https://github.com/mikeredev/dotfiles/blob/main/system-mgmt/backup-dotfiles.json)
- uses [run_function](https://github.com/mikeredev/modules/blob/main/run_function.py) custom module

### manage-screenshot
- screenshot functions to bind to hotkeys
- takes fullscreen/area screenshot, saves locally, copies image to clipboard

### rofi-gpt-chatbot
- creates a chat completion using the OpenAI API
- rofi menu to generate and return a chat completion
- uses [openai_chat](https://github.com/mikeredev/modules/blob/main/openai_chat.py) custom module

### rofi-session-manager
- rofi session manager for i3
- lock/logoff/reboot/etc.

### rofi-wifi-manager
- rofi wifi connection manager for i3