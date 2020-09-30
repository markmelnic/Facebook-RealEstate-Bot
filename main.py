import pynput.keyboard
import pynput.mouse
from pynput.mouse import Button

import random, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

MAIN_LINK = "https://www.facebook.com"
LOGIN_LINK = "https://www.facebook.com/login/"
MARKETPLACE_LINK = "https://www.facebook.com/marketplace/category/propertyrentals/"

# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./chromedriver.exe")
    dv.maximize_window()
    return dv

# kill the driver
def killb(dv):
    dv.quit()

# login protocol
def login(dv, username, password):
    dv.get(LOGIN_LINK)

    # username
    loginUsername = dv.find_element_by_name("email")

    for i in range(len(username)):
        #time.sleep(0.1)
        loginUsername.send_keys(username[i])

    # password
    loginPassword = dv.find_element_by_name("pass")
    for i in range(len(password)):
        #time.sleep(0.1)
        loginPassword.send_keys(password[i])

    # sign in
    signInClick = dv.find_element_by_name("login")
    signInClick.click()


# messaging procedure
def messagingProcedure(dv, messages, email, namesFile, processed_links):
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()

    current_window = dv.current_window_handle

    time.sleep(3)
    dv.get(MARKETPLACE_LINK)

    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(5)
    
    print("You have 15 seconds to adjust location etc...")
    #time.sleep(15)

    soup = BeautifulSoup(dv.page_source, 'html.parser')
    listings = soup.find_all("a")

    page_body = dv.find_element_by_xpath("/html/body")

    for listing in listings:
        if (listing['role'] == "link") and ("/marketplace/item/" in listing['href']):
            if not MAIN_LINK + listing['href'] in processed_links:
                processed_links.append(MAIN_LINK + listing['href'])
                namesFile.write(MAIN_LINK + listing['href'] + "\n")
                dv.execute_script('window.open(arguments[0]);', MAIN_LINK + listing['href'])
                new_window = [window for window in dv.window_handles if window != current_window][0]
                dv.switch_to.window(new_window)
                dv.implicitly_wait(5)
                ct = dv.find_element_by_xpath("//*[@id=\"mount_0_0\"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div[1]")
                ct.click()
                time.sleep(2)
                if ct.text == "Message":
                    mouse.position = (950, 650)
                    mouse.click(Button.left, 2)
                    time.sleep(0.5)
                    keyboard.type(random.choice(messages))
                    dv.find_element_by_xpath("//*[@id=\"mount_0_0\"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div").click()
                else:
                    mouse.position = (950, 475)
                    mouse.click(Button.left, 2)
                    time.sleep(0.5)
                    keyboard.type(email)
                    mouse.position = (950, 650)
                    mouse.click(Button.left, 2)
                    time.sleep(0.5)
                    keyboard.type(random.choice(messages))
                    dv.find_element_by_xpath("//*[@id=\"mount_0_0\"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/span/div").click()

                time.sleep(2)
                dv.close()
                dv.switch_to.window(current_window)
        else:
            pass


if __name__ == "__main__":
    try:
        with open("message.txt", "r") as msgFile:
            messages = msgFile.read().splitlines()
        dv = boot()

        with open("login_credentials.txt", "r", newline = '') as credsFile:
            credentials = credsFile.read().splitlines()
        login(dv, credentials[0], credentials[1])

        try:
            with open("links.txt", "r") as links_file:
                processed_links = links_file.read().splitlines()
        except:
            with open("links.txt", "w") as links_file:
                processed_links = []
                pass
        with open("links.txt", "a") as links_file:
            messagingProcedure(dv, messages, credentials[0], links_file, processed_links)

        killb(dv)
    except KeyboardInterrupt:
        killb(dv)