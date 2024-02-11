from pip import main as pip
import os , time

GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def install_package(package_name):
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{YELLOW}Installing {package_name}..." + RESET)
        pip(['install', package_name])
        print(GREEN + f"{package_name} installed successfully" + RESET)
        time.sleep(1)
    except Exception as e:
        print(RED + f"Error installing {package_name}: {e}" + RESET)

packages_to_install = ["flask", "colorama", "psutil"]
for package in packages_to_install:
    install_package(package)

os.system('cls' if os.name == 'nt' else 'clear')
print(CYAN + "Install all packages successfully done\nNow you can run "+ GREEN + "API.py " + RESET)