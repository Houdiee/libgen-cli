from libgen_api_enhanced import LibgenSearch
from prettytable import PrettyTable
import os
import sys
import subprocess
import threading
import time
import shutil
import json

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"

UNDERLINE_CYAN = "\033[4;36m"

def get_terminal_size():
    try:
        return shutil.get_terminal_size()
    except Exception:
        return 80, 20  # Fallback size

def libgen_search(query):
    results = LibgenSearch().search_default(query)
    return results

def truncate_string(s, max_length):
    return s if len(s) <= max_length else s[:max_length - 3] + '...'

def display_table(data):
    table = PrettyTable()
    # Define field names
    field_names = [
        f"{YELLOW}ID{RESET}", 
        f"{BLUE}Author{RESET}", 
        f"{GREEN}Title{RESET}",
        f"{CYAN}Publisher{RESET}", 
        f"{MAGENTA}Year{RESET}", 
        f"{MAGENTA}Pages{RESET}", 
        f"{YELLOW}Language{RESET}", 
        f"{GREEN}Size{RESET}", 
        f"{BLUE}Extension{RESET}"
    ]

    table.field_names = field_names

    columns, _ = get_terminal_size()
    
    # Set specific widths for each column
    min_column_widths = [10] * len(field_names)  # Minimum width for each column
    min_column_widths[1] = 15
    min_column_widths[2] = 55
    min_column_widths[3] = 15

    # Initial width assignment based on minimums
    column_widths = min_column_widths.copy()

    # Calculate total fixed width and remaining space
    total_fixed_width = sum(column_widths)
    remaining_space = max(columns - total_fixed_width, 0)

    # Distribute remaining space among columns
    num_adjustable_columns = len(field_names) - 1  # Exclude Title from space distribution
    for i in range(len(field_names)):
        if i != 2:  # Skip Title column
            column_widths[i] += remaining_space // num_adjustable_columns

    # Add rows to the table with truncated values
    for idx, row in enumerate(data[:25]):
        table.add_row([
            f"{YELLOW}{idx + 1}{RESET}",  # ID column (1-based index)
            truncate_string(row["Author"], column_widths[1]),
            truncate_string(row["Title"], column_widths[2]),
            truncate_string(row["Publisher"], column_widths[3]),
            truncate_string(row["Year"], column_widths[4]),
            truncate_string(row["Pages"], column_widths[5]),
            truncate_string(row["Language"], column_widths[6]),
            truncate_string(row["Size"], column_widths[7]),
            truncate_string(row["Extension"], column_widths[8])
        ])

    print(table)

def download_file(url):
    try:
        print(f"{GREEN}Downloading file...{RESET}")
        subprocess.run(["curl", "-O", "--progress-bar", url], check=True)
        print(f"{GREEN}Download completed!{RESET}")
        print()
    except subprocess.CalledProcessError:
        print(f"{RED}Error during download.{RESET}")

def loading_spinner():
    spinner = ['|', '/', '-', '\\']
    while not stop_spinner_event.is_set():
        for symbol in spinner:
            sys.stdout.write(f'\r{YELLOW}{symbol} Searching...{RESET}')
            sys.stdout.flush()
            time.sleep(0.1)

def main():
    global stop_spinner_event
    stop_spinner_event = threading.Event()
    
    search_query = input(f"{UNDERLINE_CYAN}Enter search query:{RESET} ")
    
    # Start the loading spinner in a separate thread
    spinner_thread = threading.Thread(target=loading_spinner)
    spinner_thread.start()

    try:
        data = libgen_search(search_query)

        # Stop the spinner
        stop_spinner_event.set()
        spinner_thread.join()

        print()

        if not data:
            print(f"{RED}No results found for '{search_query}'.{RESET}")
            return

        display_table(data)

        if len(data) >= 25:
            print(f"{GREEN}{len(data)} results found for '{search_query}'. Showing first 25 results.")
        else:
            print(f"{GREEN}{len(data)} results found for '{search_query}'.{RESET}")
        print()

        while True:
            selected_id = input(f"{CYAN}Enter the ID of the result you want to download (1-{len(data)}): {RESET}")
            try:
                selected_index = int(selected_id) - 1
                if selected_index < 0 or selected_index >= len(data):
                    raise ValueError("Invalid ID")
                
                download_url = data[selected_index].get("Direct_Download_Link")
                if download_url:
                    download_file(download_url)
                    break  # Exit loop after successful download
                else:
                    print(f"{RED}Download URL not found for the selected result.{RESET}")
                    continue  # Continue the loop if the URL is not found
            except ValueError:
                print(f"{RED}Invalid selection. Please enter a number between 1 and {len(data)}.{RESET}")
        
    except json.JSONDecodeError:
        stop_spinner_event.set()
        spinner_thread.join()
        print(f"\n{RED}No results found for '{search_query}'.{RESET}")
        return
    except Exception as e:
        stop_spinner_event.set()
        spinner_thread.join()
        print(f"\n{RED}An unexpected error occurred: {str(e)}{RESET}")
        return

if __name__ == "__main__":
    main()

