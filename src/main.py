#!/usr/bin/env python3
import re
import time
import smtplib
import os
import requests
from datetime import datetime 
from bs4 import BeautifulSoup

# https://stackoverflow.com/questions/48095700/web-scraping-back-in-stock-notification

def stock_check(url, div, keyword):
    """Checks url for 'sold out!' substring in add-cart-wrapper"""
    soup = BeautifulSoup(url.content, "html.parser") #Need to use lxml parser
    stock = soup.find("div", div) #Check the html tags for sold out/coming soon info.
    stock_status = re.findall(keyword, str(stock)) #Returns list of captured substring if exists.
    return stock_status # returns "Coming Soon" from soup string.

def send_email(address, password, sms_number, email_subject, message):
    """Send an e-mail to yourself!"""
    server = smtplib.SMTP("smtp.gmail.com", 587) #e-mail server
    server.ehlo()
    server.starttls()
    server.login(address,password) #login
    # message = str(message) #message to email yourself
    message = 'Subject: {}\n\n{}'.format(email_subject, str(message))
    recipients = [address,sms_number]
    server.sendmail(address,recipients,message) #send the email through dedicated server
    return

def stock_check_listener(url, address, password, sms_number, email_subject, run_hours, poll_frequency, div, keyword):
    """Periodically checks stock information."""
    listen = True # listen boolean
    start = datetime.now() # start time
    while(listen): #while listen = True, run loop
        if keyword in stock_check(url, div, keyword): #check page
            now = datetime.now()
            print(str(now) + ": Not in stock.")
        else:
            now = datetime.now()
            message = str(now) + ": NOW IN STOCK!"
            print(message)
            send_email(address, password, sms_number, email_subject, message)
            listen = False

        duration = (now - start)
        seconds = duration.total_seconds()
        hours = int(seconds/3600)

        if hours >= run_hours: #check run time
            print("Finished.")
            listen = False

        # time.sleep(30*60) #Wait N minutes to check again.    
        time.sleep(poll_frequency) #Wait N seconds to check again.    
    return

if __name__=="__main__":
    
    ## Test Variables
    # os.environ['PAGE'] = "https://fujifilm-x.registria.com/products/0-74101-20713-2"
    # os.environ['DIV'] = "pdp-buy-now-txt"
    # os.environ['KEYWORD'] = "Notify Me"
    # os.environ['EMAIL_SUBJECT'] = "!! Fujifilm Stock Update !!"

    # os.environ['PAGE'] = "https://fieldsheer.com/products/7-4v-glove-2in1-battery?variant=30238111826035"
    # os.environ['DIV'] = "add-cart-wrapper"
    # os.environ['KEYWORD'] = "Coming Soon"
    # os.environ['EMAIL_SUBJECT'] = "!! Fieldsheer Stock Update !!"

    # os.environ['ADDRESS'] = ""
    # os.environ['PASSWORD'] = ""
    # os.environ['SMS_NUMBER'] = ""

    # os.environ['RUN_HOURS'] = 2190
    # os.environ['POLL_FREQUENCY'] = 10
    
    page = os.environ.get("PAGE")
    div = os.environ.get("DIV")
    keyword = r"{}".format(os.environ.get("KEYWORD"))
    email_subject = str(os.environ.get("EMAIL_SUBJECT"))

    #Run listener to stream stock checks.
    address = os.environ.get("ADDRESS")
    password = os.environ.get("PASSWORD")
    sms_number = os.environ.get("SMS_NUMBER")

    run_hours = int(os.environ.get("RUN_HOURS"))
    poll_frequency = int(os.environ.get("POLL_FREQUENCY")) # Poll time in seconds

    #Set url and userAgent header for javascript issues.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html'}

    #URL request.
    url = requests.get(url=page,
                       headers=headers)
    
    stock_check_listener(url=url,
                         address=address,
                         password=password,
                         sms_number=sms_number,
                         email_subject=email_subject,
                         run_hours=run_hours,
                         poll_frequency=poll_frequency,
                         div=div,
                         keyword=keyword)