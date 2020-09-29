
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
def loginProc(dv, username, password):
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
    time.sleep(3)
    dv.get(MARKETPLACE_LINK)

    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(5)
    
    print("You have 15 seconds to adjust location etc...")
    #time.sleep(15)

    soup = BeautifulSoup(dv.page_source, 'html.parser')
    listings = soup.find_all("a")
    print(len(listings))

    page_body = dv.find_element_by_xpath("/html/body")
    for listing in listings:
        if listing['role'] == "link" and "/marketplace/item/" in listing['href']:
            dv.execute_script('window.open(arguments[0]);', listing['href'])
            print(listing['href'])
            #listing.click()
        else:
            continue
        page_body.send_keys(Keys.ARROW_DOWN)
        WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
        time.sleep(5)

        name = dv.find_element_by_class_name("_3cgd").text
        name = str(name.encode("utf8"))
        if not name in currentnames:
            currentnames.append(name)
            namesFile.write(name + "\n")
            
            time.sleep(3)

            textInput = dv.find_element_by_attribute("textarea")

            for i in range(19):
                textInput.send_keys(Keys.BACKSPACE)
            
            msg = str(random.choice(message))
            for i in range(len(msg)):
                #time.sleep(0.1)
                textInput.send_keys(msg[i])
            
            textInput.send_keys(Keys.ENTER)
            time.sleep(5)

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

        loginProc(dv, email, password)

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