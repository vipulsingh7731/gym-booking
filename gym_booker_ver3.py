from random import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import os
import random
from selenium.webdriver.common.alert import Alert
import getpass


print("Format: '06:00 PM', '08:30 AM', etc")
print("And you have 60secs to login When the login screen appears")
book_time = input("Input time in the exact format you want to register--")
book_date = input("Press ENTER to book for TOMORROW's date OR Type the date TO BOOK in exact format DD-MM-YYYY '01-03-2022' without quotes: ")
roll_no = input("Enter your roll no.: ")
password = getpass.getpass("Enter your password: ")
while ( getpass.getpass("Confirm your password: ") != password):
    print("You password did not match, please type again!")
    password = getpass.getpass("Enter your password: ")
auth_otp = input("Enter your Authenticator OTP: ")
browser = webdriver.Chrome()

browser.get("https://gymkhana.iitb.ac.in/~sports/index.php?r=site/gymbooking")
browser.find_element(by=By.ID, value="signin").click()
time.sleep(1)
browser.find_element(by=By.ID, value="username").send_keys(roll_no) # SSO login
browser.find_element(by=By.ID, value="password").send_keys(password)
time.sleep(1.2)
browser.find_element(by=By.NAME, value="totp").send_keys(auth_otp)
time.sleep(0.5)
browser.find_element(by=By.NAME, value="login").click() # click on login
time.sleep(1)
browser.find_element(by=By.XPATH, value='//*[@id="login-content"]/div[2]/form[1]/input[2]').click() # Click on continue

time.sleep(1)
browser.find_element(by=By.CSS_SELECTOR, value="#authorizationForm > div.form-group > div > input.btn.btn-large.btn-success").click()


if book_date=="":
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    tomorrow_string = datetime.datetime.strftime(tomorrow, f"%d-%m-%Y {book_time}") #e.g. 03-02-2022 06:00 PM
else:
    tomorrow_string = f"{book_date} {book_time}"
    
while(True):
    browser.get("https://gymkhana.iitb.ac.in/~sports/index.php?r=site/gymbooking")
    
    cards = browser.find_elements(by=By.CLASS_NAME, value="card")
    break_cond = False
    
    for card in cards:
        datetime_card = " ".join(card.text.split("\n")[1::-1]) # e.g. 02-02-2022 07:00 PM
        card_found = False
        #verify card is correct
        if datetime_card == tomorrow_string:
            try:   
                card_found = True
                if card.find_element(by=By.TAG_NAME, value="button").text == "book slot":
                    button = card.find_element(by=By.TAG_NAME, value="button")
                    button.click()
            except:
                pass
        if card_found == True:
            time.sleep(1)
            try:
                modal_content = browser.find_element(by=By.CLASS_NAME, value="modal-dialog")
                time_in_dialogue = modal_content.find_element(by=By.TAG_NAME,value="h5").text.split(" ")[-2:]
                time_in_dialogue = " ".join(time_in_dialogue) # e.g. 2022-02-03 18:00?
                object_time = datetime.datetime.strptime(time_in_dialogue, "%Y-%m-%d %H:%M?")
                time_in_dialogue = datetime.datetime.strftime(object_time, "%d-%m-%Y %I:%M %p")
            except:
                pass
            #verify time in dialogue is correct
            if tomorrow_string == time_in_dialogue:
                modal_content.find_element(value="modal-btn-yes").click()
                time.sleep(1)
                alert_obj = browser.switch_to.alert
                alert_obj.accept()
                print("Great Success!!!")
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(3)
                
                browser.close()
                break_cond = True
                break
    if break_cond == True:
        break
    # Implementation of time delays
    min_wait = random.randint(1, 10)
    if datetime.datetime.strptime(tomorrow_string, "%d-%m-%Y %I:%M %p") >= datetime.datetime.now() + datetime.timedelta(1, 60*min_wait):
        print(f"waiting {min_wait} minutes")
        time.sleep(min_wait*60)
    else: 
        print("Refreshing quickly")   
        time.sleep(0.1*random.randint(3, 7))

os.system("PAUSE")
            