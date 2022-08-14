from random import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import os
import random
from selenium.webdriver.common.alert import Alert

print("Format: '06:00 PM', '08:30 AM', etc")
print("And you have 60secs to login When the login screen appears")
my_input = input("Input time in the exact format you want to register--")
browser = webdriver.Chrome()

browser.get("https://gymkhana.iitb.ac.in/~sports/index.php?r=site/userlogin")

browser.find_element(by=By.ID, value="signin").click()
time.sleep(60)
# browser.execute("alert('Input time in python window & You have 60secs to login')")
try:
    browser.find_element(by=By.CSS_SELECTOR,value="#authorizationForm > div.form-group > div > input.btn.btn-large.btn-success").click()
except:
    pass


while(True):
    browser.get("https://gymkhana.iitb.ac.in/~sports/index.php?r=site/gymbooking")
    print(browser.window_handles[0])
    cards = browser.find_elements(by=By.CLASS_NAME, value="card")
    break_cond = False
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    tomorrow_string = datetime.datetime.strftime(tomorrow, f"%d-%m-%Y {my_input}") #e.g. 03-02-2022 06:00 PM
    # print(tomorrow_string, "yes")
    # try:
    #     if cards[0].text.split("\n")[-2] == "You have booked this slot":
    #         print("Great Success!!!")
    #         browser.close()
    #         break
    # except :
    #     pass
    for card in cards:
        datetime_card = " ".join(card.text.split("\n")[1::-1]) # e.g. 02-02-2022 07:00 PM
        card_found = False
        #verify card is correct
        if datetime_card == tomorrow_string:
            card_found = True
            if card.find_element(by=By.TAG_NAME, value="button").text == "book slot":
                button = card.find_element(by=By.TAG_NAME, value="button")
                button.click()
            
        if card_found == True:
            time.sleep(1)
            try:
                modal_content = browser.find_element(by=By.CLASS_NAME, value="modal-dialog")
                time_in_dialogue = modal_content.find_element(by=By.TAG_NAME,value="h5").text.split(" ")[-2:]
                time_in_dialogue = " ".join(time_in_dialogue) # e.g. 2022-02-03 18:00?
                object_time = datetime.datetime.strptime(time_in_dialogue, "%Y-%m-%d %H:%M?")
                time_in_dialogue = datetime.datetime.strftime(object_time, f"%d-%m-%Y %I:%M %p")
            
            except:
                pass
            #verify time in dialogue is correct
            if tomorrow_string== time_in_dialogue:
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
    min_wait = 2
    if datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(), f"%d-%m-%Y {my_input}"),"%d-%m-%Y %I:%M %p") >= datetime.datetime.now()+ datetime.timedelta(0, 60*min_wait):
        time.sleep(min_wait*60) 
    else:    
        time.sleep(0.1*random.randint(3, 10))

os.system("PAUSE")
            