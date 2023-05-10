#!/bin/bash

options=("Lock" "Logoff" "Suspend" "Reboot" "Shutdown")
chosen=$(printf '%s\n' "${options[@]}" | rofi -dmenu -matching normal -p "Manage Session")

case "$chosen" in
    "Lock")
        i3lock
        ;;
    "Logoff")
        i3-msg exit
        ;;
    "Suspend")
        i3lock && systemctl suspend
        ;;
    "Reboot")
        confirmation=$(echo -e "Yes\nNo" | rofi -dmenu -p "Are you sure you want to reboot?")
        if [[ "$confirmation" == "Yes" ]]; then
            systemctl reboot
        fi
        ;;
    "Shutdown")
        confirmation=$(echo -e "Yes\nNo" | rofi -dmenu -p "Are you sure you want to shutdown?")
        if [[ "$confirmation" == "Yes" ]]; then
            systemctl poweroff
        fi
        ;;
    *)
        exit 1
        ;;
esac
