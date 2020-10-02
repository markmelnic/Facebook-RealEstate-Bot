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
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # driver itself
    dv = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=r"./chromedriver.exe"
    )
    dv.maximize_window()
    return dv


# kill the driver
def killb(dv):
    dv.quit()


# login protocol
def login(dv, username, password):
    dv.get(LOGIN_LINK)

    # username
    username = dv.find_element_by_name("email")
    for char in username:
        username.send_keys(char)

    # password
    password = dv.find_element_by_name("pass")
    for char in password:
        password.send_keys(char)

    # sign in
    dv.find_element_by_name("login").click()


# messaging procedure
def messagingProcedure(dv, messages, links_file, processed_links):
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()

    current_window = dv.current_window_handle

    time.sleep(3)
    dv.get(MARKETPLACE_LINK)

    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(5)

    print("You have 60 seconds to adjust settings")
    time.sleep(60)

    while True:
        page_body = dv.find_element_by_xpath("/html/body")
        page_body.send_keys(Keys.PAGE_DOWN)
        soup = BeautifulSoup(dv.page_source, "html.parser")
        listings = soup.find_all("a")
        for listing in listings:
            if (listing["role"] == "link") and (
                "/marketplace/item/" in listing["href"]
            ):
                if not MAIN_LINK + listing["href"] in processed_links:
                    try:
                        processed_links.append(MAIN_LINK + listing["href"])
                        links_file.write(MAIN_LINK + listing["href"] + "\n")
                        dv.execute_script(
                            "window.open(arguments[0]);", MAIN_LINK + listing["href"]
                        )
                        new_window = [
                            window
                            for window in dv.window_handles
                            if window != current_window
                        ][0]
                        dv.switch_to.window(new_window)
                        dv.implicitly_wait(5)
                        contact_button = dv.find_element_by_xpath(
                            '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div[1]'
                        )
                        contact_button.click()
                        time.sleep(random.randint(2, 4))
                        if contact_button.text == "Message":
                            mouse.position = (950, 650)
                            mouse.click(Button.left, 2)
                            time.sleep(1)
                            keyboard.type(random.choice(messages))
                            time.sleep(1)
                            dv.find_element_by_xpath(
                                '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div'
                            ).click()

                        time.sleep(random.randint(6, 10))
                        dv.close()
                        dv.switch_to.window(current_window)
                    except AttributeError:
                        dv.close()
                        dv.switch_to.window(current_window)
            else:
                pass


if __name__ == "__main__":
    try:
        with open("message.txt", "r") as msg_file:
            messages = msg_file.read().splitlines()
        dv = boot()

        with open("login_credentials.txt", "r", newline="") as creds_file:
            creds = creds_file.read().splitlines()
        login(dv, creds[0], creds[1])

        try:
            with open("links.txt", "r") as links_file:
                processed_links = links_file.read().splitlines()
        except:
            with open("links.txt", "w") as links_file:
                processed_links = []
                pass
        with open("links.txt", "a") as links_file:
            messagingProcedure(dv, messages, links_file, processed_links)

        killb(dv)
    except KeyboardInterrupt:
        killb(dv)
