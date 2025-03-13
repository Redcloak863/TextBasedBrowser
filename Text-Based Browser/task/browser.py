import argparse
import os
import re
import requests
import shutil
from bs4 import BeautifulSoup
from colorama import Fore

'''
Note that init() isn't here. It messes up the test on HyperSkill. If you need it to
make Colorama work on your Windows machine, comment it out before running the tests.
'''

if os.access("tb_tabs", os.F_OK):
    shutil.rmtree("tb_tabs")  # Tidy up after the tester's last run.
    # Alternatively, you could handle the error later and write files anyway.
    # I think this is a better approach as it stops the error in the first place.

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="The working folder")
folder = parser.parse_args().folder
path = f'./{folder}/'  # This is where the history files will be written.

if not os.access(folder, os.F_OK):  # Create the folder if it doesn't exist.
    os.mkdir(folder)

history = []  # The list of visited websites.
link = ""
while link.lower() != "exit":
    link = input()
    if link != "exit" and link != "back":  # Is it a command?

        if re.search(r"\.[a-z]", link):  # Looks for .something pattern
            site_name = link.split('.')  # some.page.com becomes ['some', 'page', 'com']
            file_name = site_name.pop(0)  # ['some', 'page', 'com'] --> 'some'
            # www.some.page.com then www.some-other.page.com would clearly present a problem!
            if "http" not in link:
                link = "https://" + link  # Must be https://

            page = requests.get(link)  # Do browser stuff

            html = page.content

            soup = BeautifulSoup(html, 'html.parser')

            for a in soup.find_all("a"):
                a.string = "".join(Fore.BLUE + a.get_text() + Fore.RESET)
                '''
                This part is like a Sharpie. It permanently marks up the file.
                In real life, if you need an untouched copy of soup, you can re-run
                BeautifulSoup or deepcopy soup to a new variable before attacking it
                with a Sharpie.
                '''

            print(soup.get_text())

            with open(path + file_name, 'w', encoding='utf-8') as file:
                file.write(soup.get_text())
                history.append(file_name)

        else:  # The while loop will execute again.
            response = "Invalid URL"
            print(response)  # It's wordy because it was testing something else.

    else:  # It's a command
        if "exit" in link.lower():
            break  # The while loop won't execute again.
        elif "back" in link.lower():  # The while loop will execute again.
            try:
                history.pop()  # Always remove the current page.
                site_name = history.pop()  # This is the one we want.
                with open(path + site_name, 'r') as file:
                    print(file.read())
            except IndexError:
                pass  # Do nothing
