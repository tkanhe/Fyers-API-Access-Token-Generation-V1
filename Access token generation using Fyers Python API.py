import urllib.parse as urlparse
from urllib.parse import parse_qs

from fyers_api import accessToken
from fyers_api import fyersModel
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fyers = fyersModel.FyersModel()

app_id = "your_app_id"
app_secret = "your_app_secret"
username = "your_username"    # Client ID
password = "your_password"
pan = "your_pan_number"


def read_file():
    with open("token.txt", "r") as f:
        token = f.read()
    return token


def write_file(token):
    with open('token.txt', 'w') as f:
        f.write(token)


def setup():
    """Authorization"""
    app_session = accessToken.SessionModel(app_id, app_secret)
    response = app_session.auth()
    authorization_code = response['data']['authorization_code']
    app_session.set_token(authorization_code)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(app_session.generate_token())
    driver.maximize_window()

    driver.find_element_by_id('fyers_id').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('pancard').send_keys(pan)

    driver.find_element_by_xpath("//button[@id='btn_id']").click()
    WebDriverWait(driver, 20).until((EC.url_changes(driver.current_url)))

    parsed = urlparse.urlparse(driver.current_url)
    token = parse_qs(parsed.query)['access_token'][0]
    write_file(token)
    print(fyers.get_profile(token=token))


def check():
    token = read_file()
    response = fyers.get_profile(token=token)
    if 'Invalid' in response['message'] or 'not' in response['message']:
        print('Getting a access token')
        setup()
    else:
        print('You already have a access token!')
        print(fyers.get_profile(token=token))


check()
