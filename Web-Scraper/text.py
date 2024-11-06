from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = webdriver.ChromeOptions()

# 允許所有網站通知行為
chrome_options.add_experimental_option(
    "prefs", 
    {
        "profile.default_content_setting_values.notifications": 1
    }
)

# 讀取CSV檔案
df = pd.read_csv('nccu_dcard_articles_scroll.csv')

# 儲存文章內容
data_with_content = []


for index, row in df.iterrows():
    link = row['link']
    title = row['title']
    
    try:
        driver = webdriver.Chrome(options = chrome_options)
        driver.set_window_size(1000, 1000)

        driver.get(link)
        
        # 等待文章頁面載入
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-ba53eb98-0.bAJwBU'))  # 替換成文章內容的CSS選擇器
        )
        
        # 提取文章內容
        content_elements = driver.find_elements(By.CSS_SELECTOR, 'div.sc-ba53eb98-0.bAJwBU')  # 替換成實際的內容CSS選擇器
        content = "\n".join([element.text for element in content_elements])
        
        # 儲存到data_with_content列表
        data_with_content.append({
            'title': title,
            'link': link,
            'content': content
        })
        
        # 增加隨機延遲以減少被封鎖的風險
        # time.sleep(time.uniform(1, 3))

        driver.quit()
        
    except Exception as e:
        print(f"Failed to retrieve content from {link}: {e}")

# 關閉瀏覽器
driver.quit()

# 將結果轉換為DataFrame
df_with_content = pd.DataFrame(data_with_content)

# 儲存結果到CSV檔案
df_with_content.to_csv('nccu_dcard_articles_with_content.csv', index=False)

print("所有文章內容已抓取並儲存到 'nccu_dcard_articles_with_content.csv'")
