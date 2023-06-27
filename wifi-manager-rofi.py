""" rofi-wifi-manager.py
desc:       rofi wifi connection manager for i3
requires:   rofi
usage:      i3blocks signal 3 (use `pkill -RTMIN+3 i3blocks` to update the wifi block when connecting to an SSID)
i3:         bindsym $mod+m exec --no-startup-id sh -c 'python ~/data/scripts/system-mgmt/wifi-manager-rofi.py'
"""

# import modules
import subprocess

# specify theme
theme = "~/.config/rofi/themes/sidebar.rasi"


# function to run a shell command
def run_command(cmd):
    try:
        output = subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        return f"Command execution failed: {e.output.decode().strip()}"


# function to get list of detected wifi networks
def get_wifi_networks():
    try:
        output = subprocess.check_output(
            ["nmcli", "-t", "-f", "IN-USE,SSID,Signal,Security", "device", "wifi"]
        )
        networks = output.decode().strip().split("\n")
        wifi_networks = []
        for network in networks:
            in_use, ssid, signal, security = network.split(":")
            if ssid:  # Ignore SSIDs with no name
                wifi_networks.append(
                    {
                        "in_use": in_use,
                        "ssid": ssid,
                        "signal": signal,
                        "security": security,
                    }
                )
        print(wifi_networks)
        return wifi_networks
    except subprocess.CalledProcessError:
        return []


# function to connect to a wifi network
def connect_to_wifi(ssid):
    try:
        run_command(f"notify-send 'wifi manager' 'connecting to {ssid}...' -r 9003")
        subprocess.run(["nmcli", "device", "wifi", "connect", ssid], check=True)
        run_command(
            f"notify-send 'wifi manager' '{ssid} connected successfully 👍' -r 9003 -t 3000"
        )
        run_command("pkill -RTMIN+3 i3blocks")
    except subprocess.CalledProcessError as e:
        run_command(f"notify-send 'wifi manager' 'error: {e}' -r 9003")


# function to show list of SSIDs in a rofi menu
def show_wifi_menu():
    networks = get_wifi_networks()
    menu_items = []
    for network in networks:
        ssid = network["ssid"]
        signal = network["signal"]
        security = network["security"]
        if network["in_use"] == "*":
            ssid += " [*]"
        ssid_with_signal = f"{ssid} ({signal}%) [{security}]"
        menu_items.append(ssid_with_signal)

    menu_items_str = "\n".join(menu_items)

    rofi_cmd = [
        "rofi",
        "-dmenu",
        "-i",
        "-p",
        "  ",
        "-lines",
        str(len(menu_items)),
        "-theme",
        theme,
    ]
    process = subprocess.Popen(
        rofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8"
    )
    run_command("notify-send 'wifi manager' 'network scan complete' -t 1 -r 9003")
    selected_network, _ = process.communicate(input=menu_items_str)
    selected_network = selected_network.strip().split(" ")[
        0
    ]  # Remove signal strength and security if present

    if selected_network:
        connect_to_wifi(selected_network)


# main
if __name__ == "__main__":
    run_command(
        "notify-send 'wifi manager' 'scanning networks, please wait...' -r 9003"
    )
    show_wifi_menu()
