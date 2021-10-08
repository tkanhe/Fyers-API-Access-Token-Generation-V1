import requests
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
    auth = requests.post('https://api.fyers.in/api/v1/auth', json={'app_id': app_id, 'secret_key': app_secret})
    authorization_code = auth.json()['authorization_code']
    url = f'https://api.fyers.in/api/v1/genrateToken?authorization_code={authorization_code}&appId={app_id}'

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(url)
    driver.maximize_window()

    driver.find_element_by_id('fyers_id').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('pancard').send_keys(pan)

    driver.find_element_by_xpath("//button[@id='btn_id']").click()
    WebDriverWait(driver, 20).until((EC.url_changes(driver.current_url)))

    parsed = urlparse(driver.current_url)
    token = parse_qs(parsed.query)['access_token'][0]
    write_file(token)
    print(requests.get('https://api.fyers.in/api/v1/get_profile', headers={"Authorization": token}).json())


def check():
    try:
        token = read_file()
    except:
        token = 'None'
    r1 = requests.get('https://api.fyers.in/api/v1/get_profile', headers={"Authorization": token})
    if r1.json()['s'] == 'ok':
        print('You already have a access token!')
        print(r1.json())
    else:
        print('Getting a access token')
        setup()


check()
