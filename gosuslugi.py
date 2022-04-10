import time
from webbrowser import open as open_tab
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from requests import post
from json import dumps
import pickle

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Ссылка на форму записи в МВД
TARGET_LINK = "https://www.gosuslugi.ru/600300/1/form"

# Айдишники организации для post
# айдишник нужный вам следует искать в payload в девелопер консоли
# в браузере когда POST идет на https://www.gosuslugi.ru/api/lk/v1/equeue/agg/slots

eservice_id = "10000000000"
service_id = "10000000000"
organization_id = "10003000000"

gosuslugi_login = "+7903xxxxxxx"
gosuslugi_password = "1q2w3e"

def main():
    response = send_post(read_cookies())
    if response.status_code == 401:
        write_cookies(get_cookies())
        write_log('Ошибка 401. Обновлены куки.')
        main()
        return
    elif response.status_code == 200:
        length = len(response.json()['slots'])
        if length > 0:
            write_log('Есть мест: ' + str(length))
            send_notify("ОБНАРУЖЕНЫ СЛОТЫ!!11")
            open_tab(TARGET_LINK, new=1)
        else:
            print(datetime.now().strftime('%H_%M') + " " + 'Нет мест')
            write_log('Слотов нет')
            #send_notify("МЕСТ НЕТ!")
    else:
        write_log('Ошибка {0}'.format(response.status_code))


def write_cookies(cook):
    with open('/home/user/cookie.txt', 'wb') as f:
        pickle.dump(cook, f)


def read_cookies():
    with open('/home/user/cookie.txt', 'rb') as f:
        itemlist = pickle.load(f)
    raw_cookies = ''.join(['{}={}; '.format(i['name'], i['value']) for i in itemlist])
    return raw_cookies


def send_post(cookies):
    url = 'https://www.gosuslugi.ru/api/lk/v1/equeue/agg/slots'
    headers = {'Content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json', 'Cookie': cookies}
    payload = {'eserviceId': eservice_id, 'serviceId': [service_id], 'organizationId': [organization_id], 'parentOrderId': '', 'serviceCode': '', 'attributes': []}
    return post(url, data=dumps(payload), headers=headers)


def get_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--minimal')

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
    driver.get('https://esia.gosuslugi.ru/')
    driver.implicitly_wait(7)

    input_login = driver.find_element(by=By.ID, value='login')
    input_password = driver.find_element(by=By.ID, value='password')
    btn_enter = driver.find_element(By.XPATH, '//button[text()="Войти"]')

    input_login.send_keys(gosuslugi_login)
    input_password.send_keys(gosuslugi_password)
    btn_enter.click()

    driver.get(TARGET_LINK)
    time.sleep(3)
    cookies = driver.get_cookies()
    driver.close()
    return cookies


def write_log(logmsg):
    with open('/home/user/log.txt', 'a') as f:
        f.write(datetime.now().strftime('%H_%M_%d_%m_%Y') + " " + logmsg)
        f.write("\n")
        f.close()


def send_notify(msgtext):
    fromaddr = "nomad@ag.ru"
    toaddr = "nomad@yandex.ru"
    mypass = "1q2w3e"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = msgtext

    body = msgtext
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == "__main__":
    main()
