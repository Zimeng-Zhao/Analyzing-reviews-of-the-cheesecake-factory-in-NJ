
import time
import json
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=en-US")


def getRestaurantsLinks(URL,driver):
    driver.get(URL)
    # resScroll=driver.find_element(By.CSS_SELECTOR,".e07Vkf.kA9KIf")
    # driver.execute_script("arguments[0].focus();", resScroll)
    # driver.execute_script("arguments[0].scrollIntoView(true);", resScroll)
    time.sleep(5)

    resList=driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links=[]
    for res in resList:
        links.append(res.get_attribute("href"))
    return links

def getReview(URL,driver):
    import time
    driver.get(URL)
    time.sleep(10)
    address=driver.find_element(By.CSS_SELECTOR,".Io6YTe.fontBodyMedium.kR99db").text
    reviewButtons=driver.find_elements(By.CLASS_NAME,"hh2c6")
    print(reviewButtons[1].get_attribute("aria-label"))
    reviewButtons[1].click()
    time.sleep(10)
    reviewScroll=driver.find_element(By.CSS_SELECTOR,".m6QErb.DxyBCb.kA9KIf.dS8AEf")
    #reviewScroll = driver.find_element(By.CLASS_NAME, "DxyBCb")
    for i in range(5000):
        reviewScroll.send_keys(Keys.PAGE_DOWN)
    reviewBoxList=driver.find_elements(By.CLASS_NAME,"jJc9Ad")
    reviewTexts=[]
    for review in reviewBoxList:
        reviewContent=review.find_element(By.CLASS_NAME,"wiI7pd")
        reviewStar=review.find_element(By.CLASS_NAME,"kvMYJc")
        stars=reviewStar.find_elements(By.CSS_SELECTOR,".hCCjke.vzX5Ic")
        time=review.find_element(By.CLASS_NAME,"rsqaWe")
        reviewTexts.append({"time":time.text,"star":len(stars),"content":reviewContent.text})
    #return {"address":address.text,"reviews":reviewTexts}
    return {"address":address,"review":reviewTexts}



driver = webdriver.Chrome(options=chrome_options)
links=getRestaurantsLinks("https://www.google.com/maps?sca_esv=574277537&rlz=1C5MACD_enUS1017US1017&biw=1309&bih=613&output=search&q=cheesecake+factory+NJ&source=lnms&entry=mc&sa=X&ved=2ahUKEwj33qiVpf6BAxV-tIkEHY-NDXYQ0pQJegQIChAB",driver)
driver.quit()
index=0
for link in links:
    driver = webdriver.Chrome(options=chrome_options)
    reviews=getReview(link,driver)
    with open(f'data/data_full{index}.json', 'w') as file:
        json.dump(reviews, file, indent=4)
    driver.quit()
    index+=1





