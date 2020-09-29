
import random, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options

MAIN_LINK = "https://www.facebook.com/"
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
def messagingProcedure(dv, text, namesFile, currentnames):
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
        try:
            if (listing['role'] == "link") and ("/marketplace/item/" in listing['href']):
                dv.execute_script('window.open(arguments[0]);', MAIN_LINK + listing['href'])
                new_window = [window for window in dv.window_handles if window != current_window][0]
                dv.switch_to.window(new_window)
                time.sleep(5)
                try:
                    contact_button = dv.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/span/div/div[1]/div/span/span")
                    dv.close()
                    dv.switch_to.window(current_window)
                    time.sleep(2)
                    continue
                except:
                    pass
                name = dv.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[11]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/span/span/div/div/div/span").text
                name = str(name.encode("utf8"))
                if not name in currentnames:
                    currentnames.append(name)
                    namesFile.write(name + "\n")
                    time.sleep(1)

                    message_input = dv.find_element_by_tag_name("textarea")
                    for i in range(19):
                        message_input.send_keys(Keys.BACKSPACE)
                    
                    msg = str(random.choice(message))
                    for char in msg:
                        message_input.send_keys(char)
                    
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    dv.close()
                    dv.switch_to.window(current_window)
            else:
                #page_body.send_keys(Keys.ARROW_DOWN)
                #WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
                pass
        except KeyError:
            pass


# main function 
if __name__ == "__main__":

    try:
        with open("message.txt", "r") as msgFile:
            message = msgFile.read().splitlines()
        dv = boot()

        with open("login_credentials.txt", "r", newline = '') as credsFile:
            credentials = credsFile.read().splitlines()
            email = credentials[0]
            password = credentials[1]

        login(dv, email, password)

        try:
            with open("names.txt", "r") as namesFile:
                currentnames = namesFile.read().splitlines()
        except:
            with open("names.txt", "w") as namesFile:
                currentnames = []
                pass

        with open("names.txt", "a") as namesFile:
            messagingProcedure(dv, message, namesFile, currentnames)

        killb(dv)
    except KeyboardInterrupt:
        killb(dv)