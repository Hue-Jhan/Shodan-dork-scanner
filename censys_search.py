import os
import requests
from base64 import b64encode
import json
from dotenv import load_dotenv
from censys_menu import clear_screen, print_menu, print_banner

load_dotenv()
CENSYS_API_ID = os.getenv('CENSYS_API_ID')
CENSYS_API_SECRET = os.getenv('CENSYS_API_SECRET')
BASE_URL = 'https://search.censys.io/api/v2/hosts/search'


def search_censys():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    print("\033[38;2;0;255;0m         ╔════(1) Censys Search \033[0m")
    print("\033[38;2;0;230;128m         ║ \033[0m")
    query = input("\033[38;2;0;198;174m         ╠══════> Type Query: \033[0m").strip()
    print("\033[38;2;0;168;204m         ║ \033[0m")
    n_res = input("\033[38;2;0;150;215m         ╚══════> Insert number of results: \033[0m").strip()

    params = {
        'q': query,
        'per_page': n_res,
        'virtual_hosts': 'EXCLUDE',
        'sort': 'RELEVANCE'
    }
    credentials = f"{CENSYS_API_ID}:{CENSYS_API_SECRET}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(BASE_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"\n\033[38;2;0;150;215mTotal results: {data['result']['total']}")

        for hit in data['result']['hits']:
            ip = hit['ip']
            location = hit.get('location', {})
            last_updated = hit.get('last_updated_at', 'Unknown')
            autonomous_system = hit.get('autonomous_system', {})
            os_info = hit.get('operating_system', {})
            reverse_dns = hit.get('dns', {}).get('reverse_dns', {}).get('names', ['No reverse DNS'])

            os_family = os_info.get('other', [])
            if os_family:
                os_family = os_family[0].get('value', 'Unknown')
            else:
                os_family = 'Unknown'
            as_description = autonomous_system.get('description', 'Unknown')
            bgp_prefix = autonomous_system.get('bgp_prefix', 'Unknown')
            asn = autonomous_system.get('asn', 'Unknown')
            country_code = autonomous_system.get('country_code', 'Unknown')
            as_name = autonomous_system.get('name', 'Unknown')

            print(f"\n \033[38;2;0;255;0m [+] IP: {ip} \033[0m")
            print("     \033[38;2;0;230;128m Device info:\033[0m")
            print(f"        \033[38;2;0;198;174m Operating System: \033[38;2;0;150;215m{os_info.get('vendor', 'Unknown')} ({os_family}),\033[38;2;0;198;174m Autonomous System:\033[38;2;0;150;215m {as_name} ({as_description})\033[0m")
            print(f"        \033[38;2;0;198;174m ASN:\033[38;2;0;150;215m {asn},\033[38;2;0;198;174m BGP Prefix:\033[38;2;0;150;215m {bgp_prefix},\033[38;2;0;198;174m Country Code: \033[38;2;0;150;215m{country_code}\033[0m")
            print(f"        \033[38;2;0;198;174m Reverse DNS: \033[38;2;0;150;215m{', '.join(reverse_dns)}\033[0m")

            print("     \033[38;2;0;230;128m Location data:\033[0m")
            print(f"        \033[38;2;0;198;174m City:\033[38;2;0;150;215m {location.get('city', 'Unknown')},\033[38;2;0;198;174m {location.get('country', 'Unknown')}, {location.get('postal_code', 'Unknown')}\033[0m")
            print(f"        \033[38;2;0;198;174m Coordinates:\033[38;2;0;150;215m {location.get('coordinates', {}).get('latitude', 'N/A')}, {location.get('coordinates', {}).get('longitude', 'N/A')}\033[0m")
            print(f"        \033[38;2;0;198;174m Timezone:\033[38;2;0;150;215m {location.get('timezone', 'Unknown')},\033[38;2;0;198;174m Continent: \033[38;2;0;150;215m{location.get('continent', 'Unknown')}\033[0m")

            print("     \033[38;2;0;230;128m Services: \033[0m")
            for service in hit.get('services', []):
                port = service['port']
                service_name = service.get('service_name', 'Unknown')
                extended_service_name = service.get('extended_service_name', 'Unknown')
                banner = service.get('banner', 'No banner')
                if service_name.lower() != 'http' and extended_service_name.lower() != 'http':
                    http_response = service.get('http', {}).get('response', {})
                    status_code = http_response.get('status_code', 'Unknown')
                    status_reason = http_response.get('status_reason', 'Unknown')
                    http_request = service['http'].get('request', {}) if 'http' in service else {}
                    method = http_request.get('method', 'Unknown')
                    uri = http_request.get('uri', 'Unknown')
                    headers = http_request.get('headers', {})
                    user_agent = headers.get('User_Agent', ['No User-Agent'])[0]  # Assuming it's a list

                    print(f"      \033[38;2;0;230;128m- Service: \033[38;2;0;150;215m {service_name} on \033[38;2;0;230;128m port\033[38;2;0;150;215m {port}\033[0m")
                    print(f"         \033[38;2;0;230;128mBanner:\033[38;2;0;150;215m{banner.strip()}")
                    print(f"         \033[38;2;0;230;128mHTTP Status: \033[38;2;0;150;215m{status_code} - {status_reason}\033[0m")
                    print(f"         \033[38;2;0;230;128mHTTP Request Method:\033[38;2;0;150;215m {method}, URI: {uri}\033[0m")
                    print(f"         \033[38;2;0;230;128mUser-Agent: \033[38;2;0;150;215m{user_agent}\033[0m")
                else:
                    print(f"\n \033[38;2;0;230;128m     Service: \033[38;2;0;150;215m{service_name} on\033[38;2;0;230;128m port \033[38;2;0;150;215m{port}")
                    print(json.dumps(service, indent=4))

    else:
        print(f"Error: {response.status_code} - {response.text}")

    input("\nPress Enter to return to the menu...")
