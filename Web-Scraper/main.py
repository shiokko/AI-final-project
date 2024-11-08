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
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

driver = webdriver.Chrome(options = chrome_options)
driver.set_window_size(1000, 1000)

driver.get("https://www.dcard.tw/f/nccu?tab=latest")  # 設定政大討論版的URL
# 設定滾動次數，並確保頁面完全加載
scroll_pause_time = 1  # 每次滾動後停頓的時間
scroll_increment = 200  # 每次滾動的像素距離，這裡設置為小的步長來慢速滾動
scroll_times = 20

data = []
seen = set() 

for _ in range(scroll_times):
    # driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    time.sleep(scroll_pause_time)
    
    # 等待新的內容加載出來，這裡等待指定的元素出現
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.t1gihpsa')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('a', {'class': 't1gihpsa'})  # 根據你的需求調整class名稱
    for article in articles:
        title = article.get_text()  # 文章標題
        link = article['href']  # 文章連結
        full_link = f'https://www.dcard.tw{link}'  # 拼接完整的連結
    
        if full_link not in seen:
            seen.add(full_link)  # 將新連結加入set
            # 儲存抓取的資料
            data.append({
                'title': title,
                'link': full_link
            })
    
    # 等待2秒鐘來確保頁面完全加載
    # time.sleep(2)

# 將結果儲存到DataFrame
df = pd.DataFrame(data)

# 顯示結果
print(df)

# 儲存到CSV檔案
df.to_csv('nccu_dcard_articles_scroll.csv', index=False)

# 關閉瀏覽器
driver.quit()
