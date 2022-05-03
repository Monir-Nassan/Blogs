import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions

home = 'https://www.facebook.com/'


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--no-sandbox')

    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    return webdriver.Chrome(options=options)


def find(driver, by, attribute, value):
    try:
        el = WebDriverWait(driver, 10).until(
            lambda d: driver.find_element(By.XPATH,
                                            '//{by}[@{attribute}="{value}"]'.format(
                                                by=by, attribute=attribute,
                                                value=value)))
        return el
    except exceptions.TimeoutException as e:
        print(e.msg)
        return False


def check_before_login_cookies(driver):
    el = find(driver, 'button', 'class', '_42ft _4jy0 _9xo7 _4jy3 _4jy1 selected _51sy')
    if not el:
        print('cookies found after login')
        return False

    print('cookies found before login')
    el.click()


def login(driver, email, password):
    check_before_login_cookies(driver)
    email_element = find(driver, 'input', 'name', 'email')
    email_element.send_keys(email)
    password_element = find(driver, 'input', 'name', 'pass')
    password_element.send_keys(password)
    find(driver, 'button', 'name', 'login').click()
    check_after_login_cookies(driver)
    return check_home(driver)


def check_after_login_cookies(driver):
    el = find(driver, 'div', 'class',
              'l9j0dhe7 du4w35lb j83agx80 pfnyh3mw taijpn5t bp9cbjyn owycx6da btwxx1t3 kt9q3ron ak7q8e6j isp2s0ed ri5dt5u2 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv d1544ag0 tw6a2znq s1i5eluu tv7at329')
    if el:
        print('cookies found afterlogin')
        el.click()
    print('cookies not found after login')
    return False


def check_home(driver):
    driver.get(home)
    if find(driver, 'a', 'aria-label', 'Home'):
        print('login successfully')
        return True
    return False


def save_cookies(driver , filename):
    pickle.dump(driver.get_cookies(), open(filename, 'wb'))
    print("cookies saved successfully")


def add_cookies(driver, filename):
    cookies = pickle.load(open(filename, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("cookies added successfully")
    return True


def main():
    filename = "user1.pkl"
    username = ""
    password = ""
    driver = init_driver()
    driver.get(home)
    login(driver, username, password)
    save_cookies(driver, filename)
    driver.quit()

    driver = init_driver()
    driver.get(home)
    check_before_login_cookies(driver)
    add_cookies(driver, filename)
    check_after_login_cookies(driver)
    check_home(driver)
    driver.quit()


if __name__ == '__main__':
    main()
