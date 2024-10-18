import os
from dotenv import load_dotenv
import sys
import shodan
from censys_search import search_censys
from censys_get_host_info import get_host_info
from menu import print_banner, print_menu, clear_screen
from shodan_scan import shodan_info
from shodan_queries import shodan_queries


load_dotenv()
CENSYS_API_ID = os.getenv('CENSYS_API_ID')
CENSYS_API_SECRET = os.getenv('CENSYS_API_SECRET')
BASE_URL = 'https://search.censys.io/api/v2/hosts/search'
HOST_URL = 'https://search.censys.io/api/v2/hosts/'


def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        choice = input(" \033[38;2;0;140;225m           ╚══════> \033[0m").strip()
        if choice == "1":
            search_censys()
        elif choice == "2":
            get_host_info()
        elif choice == "3":
            shodan_info()
        elif choice == "4":
            shodan_queries()
        elif choice == "0":
            clear_screen()
            sys.exit()
        else:
            print("Invalid option selected.")
            input("\nPress Enter to try again...")


if __name__ == '__main__':
    main()
