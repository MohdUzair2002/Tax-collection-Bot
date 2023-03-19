from lib2to3.pgen2 import driver
from selenium import webdriver
import csv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
data1=[]
with open('All Lake County 2020 liens sold.csv','rt')as f:
  data = csv.reader(f)
  i=0
  for row in data:
        data1.append(row)
        i+=1
        print(i)
print(data1)

chrome_options = Options()
S=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=S,options=chrome_options)
i=1
f=open("Tax.csv",'w')
w=csv.writer(f)
wait = WebDriverWait(driver, 60)
while(i<len(data1)):
    url="https://tax.lakecountyil.gov/search/commonsearch.aspx?mode=realprop"
    driver.get(url)

    if (i==1):
        Agree_button=wait.until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Agree')]")))
        Agree_button.click()
        
    parcel_id=wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@aria-label='Parcel ID']")))
    parcel_id=driver.find_element(By.XPATH,"//*[@aria-label='Parcel ID']")
    print(data1[i][1])
    parcel_id.send_keys(data1[i][1])
    search_button=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Search')]")))
    search_button=driver.find_element(By.XPATH,"//button[contains(text(),'Search')]")
    driver.execute_script("arguments[0].click();", search_button)
    try:
        person=wait.until(EC.element_to_be_clickable((By.XPATH,"//tr[@class='SearchResults']")))
        person=driver.find_element(By.XPATH,"//tr[@class='SearchResults']")
        driver.execute_script("arguments[0].click();", person)
    except:
        pass
    time.sleep(4)
    name=driver.find_element(By.XPATH,"//td[@class='DataletHeaderBottom']")
    print(name.text)
    address=driver.find_elements(By.XPATH,"//td[@class='DataletHeaderBottom']")[-1]
    print(address.text)
    Assesmentyear=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[1]/table[2]/tbody/tr[2]/td[2]")
    print(Assesmentyear.text)
    Property_use_code=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[1]/table[2]/tbody/tr[15]/td[2]")
    print(Property_use_code.text)
    Tax_Year=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[1]/td[2]")
    print(Tax_Year.text)
    try:
        In_Forfeiture=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[2]/td[2]")
        print(In_Forfeiture.text)
    except:
        pass
    try:
     In_Bankcruptuncy=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[3]/td[2]")
     print(In_Bankcruptuncy.text)
    except:
        pass
    try:
     Taxe_Dues=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[4]/td[2]")
     print(Taxe_Dues.text)
    except:
        pass
    try:
     Tax_Lien_on_Property=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[5]/td[2]")
     print(Tax_Lien_on_Property.text)
    except:
        pass
    try:
     Tax_Adjustment=driver.find_element(By.XPATH,"/html/body/div/div[3]/section/div/form/div[3]/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/table[2]/tbody/tr[6]/td[2]")
     print(Tax_Adjustment.text)
    except:
        pass
   
    w.writerow([name.text, address.text])
    f.flush()

    time.sleep(4)

    i+=1
    
         