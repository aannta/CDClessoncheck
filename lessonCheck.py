#! python3
# check CDC website for slot availability of practical lessons and tests

import time, webbrowser, datetime, smtplib, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

LINK = 'https://www.cdc.com.sg/'
CDCUSERNAME = '00000000'
CDCPASSWORD = 'psswd'
DOMAIN = 'smtp.mail.yahoo.com'
PORT = 587
EMAILUSERNAME = 'emailfrom@yahoo.com'
EMAILPASSWORD = 'psswd'
EMAILSENDTO = 'emailto@yahoo.com'

def sendEmail(emailSubject, emailBody):
    conn = smtplib.SMTP(DOMAIN, PORT)
    conn.ehlo()
    conn.starttls()
    conn.login(EMAILUSERNAME, EMAILPASSWORD)
    conn.sendmail(EMAILUSERNAME, EMAILSENDTO, 'Subject: ' + emailSubject + '\n\n' + emailBody + '\n\n')
    conn.quit()

# main program

now = datetime.datetime.now()

try:
    browser = webdriver.Chrome()
except Exception as err:
    sendEmail('ChromeDriver failed', 'Exception occurred: ' + str(err) + ' at ' + now.strftime("%Y-%m-%d %H:%M"))
    sys.exit()

browser.get(LINK)
time.sleep(5)

# assign wait object
wait = WebDriverWait(browser, 20)

# find Sign-In button to click
signInElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#top-menu > ul > li.item-119 > a')))
signInElem.click()

# log in
usernameElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userId')))
usernameElem.send_keys(CDCUSERNAME)
passwordElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
passwordElem.send_keys(CDCPASSWORD)
submitElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#BTNSERVICE')))
submitElem.click()

# check practical lesson slots
menuLessonElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_Menu1_TreeView1t6')))
menuLessonElem.click()
time.sleep(1)
class3AElem = browser.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_ddlCourse > option:nth-child(2)')
class3AElem.click()
time.sleep(1)
numLessonElem = browser.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_lblSessionNo')
numLesson = int(numLessonElem.text)

# check practical test slots
menuTestElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_Menu1_TreeView1t8')))
menuTestElem.click()
time.sleep(1)
checkboxElem = browser.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_chkTermsAndCond')
checkboxElem.click()
agreeElem = browser.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_btnAgreeTerms')
agreeElem.click()
time.sleep(1)
numTestElem = browser.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_lblSessionNo')
numTest = int(numTestElem.text)

browser.quit()

# send email if there's any lesson
if numLesson != 0 or numTest != 0:    
    sendEmail('SLOT(S) AVAILABLE!!!', 'Some slot(s) available at ' + now.strftime("%Y-%m-%d %H:%M"))
else:
    sendEmail('No slot(s) available', 'No slot(s) available at ' + now.strftime("%Y-%m-%d %H:%M"))
