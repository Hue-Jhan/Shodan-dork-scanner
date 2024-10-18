import os
import requests
from base64 import b64encode
from dotenv import load_dotenv
import json
from menu import print_menu, print_banner, clear_screen

load_dotenv()
CENSYS_API_ID = os.getenv('CENSYS_API_ID')
CENSYS_API_SECRET = os.getenv('CENSYS_API_SECRET')
HOST_URL = 'https://search.censys.io/api/v2/hosts/'


def get_host_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    print("\033[38;2;0;255;0m         ╔════(1) Advanced Host Info \033[0m")
    print("\033[38;2;0;230;128m         ║ \033[0m")
    ip = input("\033[38;2;0;230;255m         ╚══════> Enter the IP address: \033[0m").strip()

    credentials = f"{CENSYS_API_ID}:{CENSYS_API_SECRET}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(f"{HOST_URL}{ip}", headers=headers)

    if response.status_code == 200:
        data = response.json().get('result', {})  # Accessing 'result' from the response
        print(f"\n\033[38;2;0;150;215mHost Information for {ip}:\033[0m")
        print("\n\033[38;2;0;230;128mDevice info:\033[0m")
        os_info = data.get('operating_system', {})
        print(f"    \033[38;2;0;198;174mOperating System:\033[0m \033[38;2;0;150;215m{os_info.get('vendor', 'Unknown')} - {os_info.get('product', 'Unknown')}\033[0m")
        as_info = data.get('autonomous_system', {})
        print(f"    \033[38;2;0;198;174mAutonomous System:\033[0m \033[38;2;0;150;215m{as_info.get('name', 'Unknown')} ({as_info.get('description', 'Unknown')})\033[0m")
        print(f"    \033[38;2;0;198;174mASN:\033[0m \033[38;2;0;150;215m{as_info.get('asn', 'Unknown')}, Country: {as_info.get('country_code', 'Unknown')}\033[0m")
        dns_names = data.get('dns', {}).get('names', [])
        print(f"    \033[38;2;0;198;174mDNS:\033[0m \033[38;2;0;150;215m{', '.join(dns_names) if dns_names else 'No DNS records'}\033[0m")
        print(f"    \033[38;2;0;198;174mLast Updated:\033[0m \033[38;2;0;150;215m{data.get('last_updated_at', 'Unknown')}\033[0m")

        print("\033[38;2;0;230;128mServices:\033[0m")
        for service in data.get('services', []):
            port = service.get('port', 'Unknown')
            service_name = service.get('extended_service_name', 'Unknown')
            banner = service.get('banner', 'No banner')

            if 'http' in service:
                http_response = service['http'].get('response', {})
                status_code = http_response.get('status_code', 'Unknown')
                status_reason = http_response.get('status_reason', 'Unknown')
                http_request = service['http'].get('request', {})
                method = http_request.get('method', 'Unknown')
                uri = http_request.get('uri', 'Unknown')
                headers = http_request.get('headers', {})
                user_agent = headers.get('User_Agent', ['No User-Agent'])[0]  # Assuming it's a list

                print(f"\n\033[38;2;0;230;128m - Service:\033[0m \033[38;2;0;150;215m{service_name} on port {port}\033[0m")
                print(f"    \033[38;2;0;230;128mBanner:\033[0m \033[38;2;0;150;215m{banner.strip()}\033[0m")
                print(f"    \033[38;2;0;230;128mHTTP Status:\033[0m \033[38;2;0;150;215m{status_code} - {status_reason}\033[0m")
                print(f"    \033[38;2;0;230;128mHTTP Request Method:\033[0m \033[38;2;0;150;215m{method}, URI: {uri}\033[0m")
                print(f"    \033[38;2;0;230;128mUser-Agent:\033[0m \033[38;2;0;150;215m{user_agent}\033[0m")
            else:
                print(f"\n\033[38;2;0;230;128mService:\033[0m \033[38;2;0;150;215m{service_name} on\033[38;2;0;230;128m port {port} \033[38;2;0;150;215m")
                print(json.dumps(service, indent=4))

    else:
        print(f"\033[38;2;255;0;0mError fetching host info: {response.status_code} - {response.text}\033[0m")

    input("\nPress Enter to return to the menu...")
