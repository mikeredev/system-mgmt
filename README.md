## system management tools
- all tools designed for i3 on arch
- some tools use custom modules from the `modules` repo
- any rofi custom themes are in the `dotfiles` repo

### backup-dotfiles
- check selected files for changes and copy them to another folder
- configured by [backup-dotfiles.json](https://github.com/mikeredev/dotfiles/blob/main/system-mgmt/backup-dotfiles.json)
- uses custom module

### manage-screenshot
- screenshot functions to bind to hotkeys
- takes fullscreen/area screenshot, saves locally, copies image to clipboard

### rofi-session-manager
- rofi session manager for i3
- lock/logoff/reboot/etc.

### rofi-wifi-manager
- rofi wifi connection manager for i3

### rofi-gpt-chatbot
- creates a chat completion using the OpenAI API
- rofi menu to generate and return a chat completion