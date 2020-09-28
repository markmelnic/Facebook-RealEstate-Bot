
import random, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options


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
    dv.get("https://www.facebook.com/login/")

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
    dv.get("https://www.facebook.com/marketplace/category/propertyrentals/")

    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(5)
    
    print("You have 15 seconds to adjust location etc...")
    #time.sleep(15)

    listings = dv.find_elements_by_class_name("_1oem")
    listings = dv.find_elements_by_tag_name("a")
    
    for listing in listings:
        scrollDown = dv.find_element_by_xpath("/html/body")
        while True:
            try:
                if listing.get_attribute('role') == "link":
                    if "/marketplace/item/" in listing.get_attribute('href'):
                        listing.click()
                    else:
                        continue
                else:
                    continue
                break
            except:
                scrollDown.send_keys(Keys.ARROW_DOWN)
        WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
        time.sleep(5)

        try:
            name = dv.find_element_by_class_name("_3cgd").text
            name = str(name.encode("utf8"))
            if not name in currentnames:
                currentnames.append(name)
                namesFile.write(name + "\n")
                
                time.sleep(3)

                i = 0
                while i < 20:
                    i += 1
                    try:
                        xpath = "/html/body/div[" + str(i) + "]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[1]/div/span/input"
                        print(xpath)
                        
                        textInput = dv.find_element_by_xpath(xpath)
                        break
                    except:
                        pass

                for i in range(19):
                    textInput.send_keys(Keys.BACKSPACE)
                
                msg = str(random.choice(message))
                for i in range(len(msg)):
                    #time.sleep(0.1)
                    textInput.send_keys(msg[i])
                
                textInput.send_keys(Keys.ENTER)
                time.sleep(5)
                
                goBack = dv.find_element_by_xpath("/html/body")
                goBack.send_keys(Keys.ESCAPE)
                
                time.sleep(2)
                try:
                    goBack.send_keys(Keys.ESCAPE)
                    time.sleep(2)
                except:
                    None
            else:
                goBack = dv.find_element_by_xpath("/html/body")
                try:
                    goBack.send_keys(Keys.ESCAPE)
                    time.sleep(2)
                except:
                    None
        except:
            goBack = dv.find_element_by_xpath("/html/body")
            try:
                goBack.send_keys(Keys.ESCAPE)
                time.sleep(2)
            except:
                None
            goBack.send_keys(Keys.ESCAPE)
            time.sleep(2)
            None
            
        
    
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
                namesFile.close()
        except:
            with open("names.txt", "w") as namesFile:
                currentnames = []
                pass

        with open("names.txt", "a") as namesFile:
            messagingProcedure(dv, message, namesFile, currentnames)
            namesFile.close()

        killb(dv)
    except KeyboardInterrupt:
        killb(dv)