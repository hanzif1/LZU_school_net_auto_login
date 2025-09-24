import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import subprocess
from requests.exceptions import ReadTimeout

# 用户名和密码变量
username = "zhanghao@lzu.edu.cn"
password = "mima"
# 设置Chrome驱动路径
chrome_driver_paths = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'  # 替换为实际的chromedriver路径

def check_internet_connection(url="https://www.baidu.com", timeout=1):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except (requests.ConnectionError, ReadTimeout):
        return False

def kill_chromedriver():
    try:
        # 确保所有chromedriver进程被终止
        subprocess.call(["taskkill", "/F", "/IM", "chromedriver.exe", "/T"], stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error killing chromedriver: {e}")

def get_current_ssid():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True, encoding="utf-8")
        for line in result.split("\n"):
            if "SSID" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error getting current SSID: {e}")
    return None

def connect_to_wifi(profile_names):
    for profile_name in profile_names:
        try:
            subprocess.call(["netsh", "wlan", "connect", f"name={profile_name}"])
            time.sleep(6)  # 等待连接完成
            current_ssid = get_current_ssid()
            if current_ssid == profile_name:
                print(f"成功连接到 {profile_name}")
                return True
        except Exception as e:
            print(f"Error connecting to WiFi: {e}")
    return False


def auto_login():
    # 检查是否连接到指定的SSID
    current_ssid = get_current_ssid()
    if current_ssid not in ["LZU", "iLZU"]:
        print(f"当前未连接到LZU或iLZU WiFi，当前连接的是 {current_ssid}，尝试连接到LZU或iLZU")
        if not connect_to_wifi(["iLZU", "LZU"]):
            print("无法连接到LZU或iLZU WiFi，请检查网络设置。")
            exit()

    # 再次检查是否已经连接到LZU或iLZU WiFi
    current_ssid = get_current_ssid()
    if current_ssid not in ["LZU", "iLZU"]:
        print("无法连接到LZU或iLZU WiFi，请检查网络设置。")
    else:
        print(f"已经连接到 {current_ssid} WiFi，继续执行后续代码")

        # 检查是否有网络连接
        if check_internet_connection():
            print("已经连接到互联网")
        else:
            print("没有网络连接，尝试登录校园网")

            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

            # 设置Chrome驱动路径
            chrome_driver_path = chrome_driver_paths

            # 创建浏览器驱动
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            try:
                # 打开校园网登录页面
                driver.get("http://10.10.0.166/")

                # 设置窗口大小
                driver.set_window_size(868, 1020)

                # 等待页面加载
                time.sleep(2)

                # 点击第二个标签
                tab_item = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".tab-item:nth-child(2)"))
                )
                tab_item.click()

                # 1. 点击模拟的下拉框 (div.select-selected) 来展开选项
                select_selected = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".custom-select .select-selected"))
                )
                select_selected.click()

                # 2. 点击 "@eLearning" 对应的选项
                # HTML: <div data-value="@study" ZgotmplZ>@eLearning</div>
                domain_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='@eLearning']"))
                )
                domain_option.click()
                # 注意：原代码的 domain_dropdown.click() 步骤被拆分成这两步

                # 输入账号
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                username_field.click()
                username_field.send_keys(username)

                # 输入密码
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                password_field.click()
                password_field.send_keys(password)

                # 点击登录按钮，使用新的 ID: login-account
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "login-account")) # ID 已修改
                )
                login_button.click()

                # 等待登录完成
                time.sleep(1)

                # 使用 check_internet_connection 函数来验证是否成功连接到互联网
                if check_internet_connection():
                    print("登录成功并连接到互联网")
                else:
                    print("登录失败或未连接到互联网")

            finally:
                # 关闭浏览器
                driver.quit()
                # 确保所有chromedriver进程被终止
                kill_chromedriver()



while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("-" * 40)
        print(f"[{current_time}] 正在进行网络连接检测...")
        
        # 调用更鲁棒的检查函数
        if not check_internet_connection():
            print("连接失败/不稳定，开始执行自动登录脚本。")
            auto_login()
        else:
            print("连接成功，一切正常。")

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] 等待5分钟后进行下一次检查...")
        time.sleep(300)