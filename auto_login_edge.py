import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import subprocess
from requests.exceptions import ReadTimeout

# 用户名和密码变量
username = ""  #不需要@lzu.edu.cn后缀
password = ""
# 下载地址  https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH
edge_driver_path = r'D:\Python\LZU_school_net_auto_login-main\chromedriver-win64\msedgedriver.exe'  # 设置 Edge 驱动路径（你下载的 msedgedriver.exe）

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

            # 配置 Edge 选项
            edge_options = Options()
            edge_options.add_argument("--headless")  # 无头模式
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--no-sandbox")

            # 设置 Edge 驱动路径（你下载的 msedgedriver.exe）
            edge_driver_path = edge_driver_path

            # 创建 Edge 浏览器驱动
            service = Service(edge_driver_path)
            driver = webdriver.Edge(service=service, options=edge_options)  # ← 使用 Edge

            try:
                driver.get("http://10.10.0.166/")

                driver.set_window_size(868, 1020)
                time.sleep(2)

                # 点击第二个标签
                tab_item = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".tab-item:nth-child(2)"))
                )
                tab_item.click()

                # 点击下拉框
                select_selected = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".custom-select .select-selected"))
                )
                select_selected.click()

                # 选择 @eLearning
                domain_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='@eLearning']"))
                )
                domain_option.click()

                # 输入账号密码
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                username_field.send_keys(username)

                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                password_field.send_keys(password)

                # 点击登录
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "login-account"))
                )
                login_button.click()

                time.sleep(1)

                if check_internet_connection():
                    print("登录成功并连接到互联网")
                else:
                    print("登录失败或未连接到互联网")

            finally:
                driver.quit()
                # 可选：杀掉 msedgedriver 进程（如果需要）
                try:
                    subprocess.call(["taskkill", "/F", "/IM", "msedgedriver.exe", "/T"], stderr=subprocess.DEVNULL)
                except:
                    pass



while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("-" * 40)
        print(f"[{current_time}] 正在进行网络连接检测...")
        
        # 调用更鲁棒的检查函数
        if not check_internet_connection():
            print("连接失败/不稳定，开始执行自动登录脚本。")
            auto_login()
        else:
            current_ssid = get_current_ssid()
            if current_ssid not in ["LZU", "iLZU"]:
                print("无需连接校园网。")
                exit()

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] 等待5分钟后进行下一次检查...")
        time.sleep(300)