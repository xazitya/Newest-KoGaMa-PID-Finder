import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
from datetime import datetime
import pytz

# Initialize colorama
init(autoreset=True)

def check_profile(profile_id):
    url = f"https://www.kogama.com/profile/{profile_id}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        return False, None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tags = soup.find_all('script')
    created_date = None
    
    for script in script_tags:
        if 'options.breadcrumb' in script.text:
            start = script.text.find('options.breadcrumb = ') + len('options.breadcrumb = ')
            end = script.text.find(';', start)
            breadcrumb = script.text[start:end].strip()
            if breadcrumb == 'null':
                return False, None, None
            else:
                breadcrumb_data = eval(breadcrumb)
                if '"created":' in script.text:
                    created_start = script.text.find('"created":') + len('"created":')
                    created_end = script.text.find(',', created_start)
                    created_date = script.text[created_start:created_end].strip().strip('"')
                return True, breadcrumb_data[0] if breadcrumb_data else None, created_date
        
    
    return False, None, None

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    system_tz = datetime.now().astimezone().tzinfo
    date_obj = date_obj.astimezone(system_tz)
    return date_obj.strftime('%d/%m/%Y %H:%M:%S %Z')

def calculate_step(delta_hours):
    if delta_hours > 6000:      
        return 13000    # (skips 13000 profiles if the profile was created more than 6000 hours ago)
    elif delta_hours > 4000:
        return 9000
    elif delta_hours > 2000:
        return 7000     
    elif delta_hours > 1000:
        return 4000
    elif delta_hours > 500:
        return 3500
    elif delta_hours > 100:
        return 2500
    elif delta_hours > 80:
        return 900
    elif delta_hours > 70:
        return 700
    elif delta_hours > 50:
        return 500      # you may need to lower certain algorythm's values (if no profiles were created in that amount of hours)
    elif delta_hours > 60:
        return 500
    elif delta_hours > 40:
        return 500
    elif delta_hours > 30:
        return 500
    elif delta_hours > 20:
        return 350
    elif delta_hours > 15:
        return 150
    elif delta_hours > 10:
        return 70
    elif delta_hours > 5:
        return 60
    elif delta_hours > 3:  
        return 55
    elif delta_hours > 2: 
        return 25
    elif delta_hours > 1:  
        return 15
    elif delta_hours > 0.5:  
        return 5
    else:
        return 100

def guess_newest_profile():
    current_id = 670183725  # set the newest ID you know for it to be faster
    search_window_hours = 0.50  # look for profiles created in the last 30 mins
    
    while True:
        created, _, created_date = check_profile(current_id)
        if created:
            if created_date:
                
                created_datetime = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%S%z')
                current_datetime = datetime.now(pytz.utc)
                delta_hours = (current_datetime - created_datetime).total_seconds() / 3600
                
                if delta_hours <= search_window_hours:
                    if delta_hours <= 0.17: 
                        print(Fore.RED + f"Found a recent profile: www.kogama.com/profile/{current_id}/ Created on: {format_date(created_date)}")
                        return current_id
                    else:
                        print(Fore.YELLOW + f"Profile {current_id} created {delta_hours:.2f} hours ago, searching further...")
                else:
                    print(Fore.YELLOW + f"Profile {current_id} created {delta_hours:.2f} hours ago, searching further...")
        
        if delta_hours > search_window_hours:
            step = calculate_step(delta_hours)
            current_id += step
        else:
            current_id += 1
    
    return None

def monitor_profiles(start_id):
    profile_id = start_id
    while True:
        created, breadcrumb_data, created_date = check_profile(profile_id)
        if created:
            formatted_date = format_date(created_date) if created_date else "N/A"
            print(Fore.GREEN + "Profile created: " + Fore.BLUE + f"www.kogama.com/profile/{profile_id}/ " + Fore.GREEN + "Username: " + Fore.BLUE + f"{breadcrumb_data['title']} " + Fore.GREEN + "Created on: " + Fore.LIGHTBLACK_EX + f"{formatted_date}")
            profile_id += 1

def get_last_ping_from_profile(profile_input):
    if profile_input.isdigit():
        profile_link = f"https://www.kogama.com/profile/{profile_input}/"
    else:
        profile_link = profile_input
        
    response = requests.get(profile_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')
        for script in script_tags:
            if '"last_ping":' in script.text:
                start = script.text.find('"last_ping":') + len('"last_ping":')
                end = script.text.find(',', start)
                last_ping = script.text[start:end].strip().strip('"')
                last_ping_datetime = datetime.strptime(last_ping, '%Y-%m-%dT%H:%M:%S%z')
                system_tz = datetime.now().astimezone().tzinfo
                last_ping_local = last_ping_datetime.astimezone(system_tz)
                return last_ping_local.strftime('%d/%m/%Y %H:%M:%S %Z')
    return "N/A"


if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print(Fore.BLUE + "1. Enter starting profile ID manually")
        print(Fore.BLUE + "2. Try to guess the newest profile ID")
        print(Fore.BLUE + "3. Check when a profile was online")
        print(Fore.RED + "4. Exit")
        print(" ")
        option = input(Fore.MAGENTA + "Select an option: ")
        
        if option == '1':
            starting_profile_id = int(input("Enter the starting profile ID: "))
            monitor_profiles(starting_profile_id)
        elif option == '2':
            latest_profile_id = guess_newest_profile()
            if latest_profile_id:
                monitor_profiles(latest_profile_id)
        elif option == '3':
            profile_link = input("Enter the profile link or ID: ")
            last_ping = get_last_ping_from_profile(profile_link)
            print(Fore.GREEN + f"Last online: {last_ping}")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")
        elif option == '4':
            break
        else:
            print("Invalid option.")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")
