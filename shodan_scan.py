import shodan
import os
from dotenv import load_dotenv
from censys_menu import clear_screen, print_menu, print_banner

api_key = os.getenv('shodan_key2')


def shodan_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    print("\033[38;2;0;255;0m         ╔════(3) Shodan Host Info \033[0m")
    print("\033[38;2;0;230;128m         ║ \033[0m")
    ip_address = input("\033[38;2;0;230;255m         ╚══════> Enter the IP address: \033[0m").strip()
    try:
        api = shodan.Shodan(api_key)
        result = api.host(ip_address)
        print_shodan_info(result)
        input("\nPress Enter to return to the menu...")
    except shodan.APIError as e:
        print(f"Error: {e}")
        return None


def print_shodan_info(data):
    if data is None:
        print("\033[38;2;0;150;215m No data to display.\033[0m")
        return

    print(f"\033[38;2;0;255;0mIP: \033[38;2;0;150;215m{data.get('ip_str')}")
    print("\033[38;2;0;255;0mDevice and host info:")
    print(f"    \033[38;2;0;198;174mCity: \033[38;2;0;150;215m{data.get('city')}")
    print(f"    \033[38;2;0;198;174mRegion: \033[38;2;0;150;215m{data.get('region_code')}")
    print(f"    \033[38;2;0;198;174mCountry: \033[38;2;0;150;215m{data.get('country_name')}")
    print(f"    \033[38;2;0;198;174mISP: \033[38;2;0;150;215m{data.get('isp')}")
    print(f"    \033[38;2;0;198;174mOrganization: \033[38;2;0;150;215m{data.get('org')}")
    print(f"    \033[38;2;0;198;174mLast Update: \033[38;2;0;150;215m{data.get('last_update')}")
    print(f"    \033[38;2;0;198;174mCoordinates: \033[38;2;0;150;215m{data.get('latitude')}, \033[38;2;0;150;215m{data.get('longitude')}")
    print(f"    \033[38;2;0;198;174mPorts: \033[38;2;0;150;215m{data.get('ports')}")
    print(f"    \033[38;2;0;198;174mHostnames: \033[38;2;0;150;215m{data.get('hostnames')}")
    print(f"    \033[38;2;0;198;174mDomains: \033[38;2;0;150;215m{data.get('domains')}")

    if 'data' in data:
        print("\n\033[38;2;0;255;0mServices:\033[38;2;0;150;215m")
        for service in data['data']:
            print(f"\n\033[38;2;0;198;174mService on port: \033[38;2;0;150;215m{service.get('port')}: \033[38;2;0;150;215m{service.get('data')}")

    if 'vulns' in data.get('opts', {}):
        print("\n\033[38;2;0;230;128mVulnerabilities:\033[38;2;0;150;215m")
        for vuln in data['opts']['vulns']:
            print(f"\033[38;2;0;198;174m - \033[38;2;0;150;215m{vuln}")

