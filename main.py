
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options
import random
import time
import csv

# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"C:\Users\markh\OneDrive\Documents\vscode projx\Facebook-RealEstate-Bot\chromedriver81.exe")
    return dv

# kill the driver
def killb(dv):
    dv.quit()
    
# login protocol
def loginProc(dv, username, password):
    dv.get("https://www.facebook.com/marketplace/propertyforsale/")

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
    signInClick = dv.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[3]/label/input")
    signInClick.click()


# messaging procedure
def messagingProcedure(dv, text, namesFile, currentnames):
    time.sleep(5)
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)

    listings = dv.find_elements_by_class_name("_1oem")
    print(listings)
    
    for listing in listings:
        listing.click()
        WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
        time.sleep(5)
        
        try:
            closeChat = dv.find_element_by_class_name("_7jbw _4vu4 button")
        except:
            None
        
        name = dv.find_element_by_class_name("_3cgd").text
        name = str(name.encode("utf8"))
        if not name in currentnames:
            currentnames.append(name)
            namesFile.write(name + "\n")
            
            time.sleep(3)

            i = 0
            while True:
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
            
            for i in range(len(message)):
                #time.sleep(0.1)
                textInput.send_keys(message[i])
            
            textInput.send_keys(Keys.ENTER)
            time.sleep(1)
            
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
        
    
# main function 
if __name__ == "__main__":
        
    with open("message.txt", "r") as msgFile:
        message = msgFile.read()
    print(message)
    
    dv = boot()
    
    with open("login_credentials.txt", "r", newline = '') as credsFile:
        credentials = credsFile.read().splitlines()
        email = credentials[0]
        password = credentials[1]
    print(credentials)

    loginProc(dv, email, password)

    with open("names.txt", "r") as namesFile:
        currentnames = namesFile.read().splitlines()
        namesFile.close()
        
    with open("names.txt", "a") as namesFile:
        messagingProcedure(dv, message, namesFile, currentnames)
        namesFile.close()
        
    killb(dv)