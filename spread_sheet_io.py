import time
#from selenium import webdriver
from seleniumwire import webdriver
from selenium_bot import get_details, perform_search
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from proxy_selector import *
from shoe_size_auxiliray import *

scopes = [
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/spreadsheets"
          ]

credentials = ServiceAccountCredentials.from_json_keyfile_name('google_keys/google_keys_good.json',scopes)
client = gspread.authorize(credentials)

target_sheet = client.open("Sneaker Test Sheet").worksheet('Sheet1')



def read_data():
    records_data = target_sheet.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    #print(records_df['Stock X URL'])
    return records_df


def generate_url(string):
    base_string = 'https://stockx.com/'
    split_string = string.split(' ')
    for word in split_string:

        ##eliminating special characters here, maybe improve it?
        word = word.strip('(')
        word = word.strip(')')

        word = word.lower() #for more accurate link

        if 'jordan' in word or 'Jordan' in word:
            base_string = base_string + 'air-'

        base_string = base_string + word + '-'


    #for the last - in string
    base_string = base_string.strip('-')
    print("Url generated:",base_string)
    return base_string




def convert_currency(price):
    number = 0
    for i in price:
        if i.isdigit():
            number = number * 10 + int(i)
    return number * 0.71


def update_stylesheet(index, url,prices,release_date,colorway,retail_price):
    #prices[0] = convert_currency(prices[0])
    #prices[1] = convert_currency(prices[1])
    shoe_name = url[19:]
    retail_price = convert_currency(retail_price)
    target_sheet.update_cell(index + 2, 4, prices[0])
    target_sheet.update_cell(index + 2, 5, prices[1])
    target_sheet.update_cell(index + 2, 6, url)
    time.sleep(1)
    target_sheet.update_cell(index + 2, 7, shoe_name)
    target_sheet.update_cell(index + 2, 8, release_date)
    target_sheet.update_cell(index + 2, 9, colorway)
    target_sheet.update_cell(index + 2, 10, retail_price)
    print('GOOGLE SPREAD SHEET UPDATE PERFORMED!')




def itterate_shoes(data,driver):
    for index, row in data.iterrows():
        #for the program not to crash when you add a new shoe and did not complete all the lines in time, low probability, tough
        if row['Style'] == "" or row['Size'] == "" or row['Type'] == "":
            pass
        else:
            if row['Stock X URL'] == "":
                if (row['Shoe Name'] != ""):
                    size = row['Size']
                    type = row['Type']
                    size = calculate_size(size,type)

                    url = generate_url(row['Shoe Name'])
                    (prices, style, colorway, retail_price, release_date, ok) = get_details(driver, url,size)

                    if prices == []: #preventing stockx 404 bug
                        pass
                    else:
                        if ok == True:
                            update_stylesheet(index,url,prices,release_date,colorway,retail_price)
                            print(f"{row['Shoe Name']} :updated URL and done!")
                else:#we need to calculate the url trough searching on stockx
                    style = row['Style']
                    search_url = 'https://stockx.com/search/sneakers?s=' + str(style)
                    shoe_url = perform_search(driver,search_url)

                    if shoe_url == "":
                        pass
                        print(style,"not found on stockx")
                    else:

                        type = row['Type']
                        size = calculate_size(row['Size'],type)

                        (prices, style, colorway, retail_price, release_date, ok) = get_details(driver, shoe_url, size)
                        if prices == []:  # preventing stockx 404 bug
                            pass
                        else:
                            if ok == True:
                                update_stylesheet(index,shoe_url,prices,release_date,colorway,retail_price)
                                print(f"{row['Shoe Name']} :updated URL and done!")

            else:
                url = row['Stock X URL']
                size = row['Size']
                type = row['Type']
                #check for size problems!!
                size = calculate_size(size,type)
                (prices, style, colorway, retail_price, release_date, ok) = get_details(driver, url, size)
                if prices == []: #preventing stockx 404 bug
                    pass
                else:
                    if ok == True:
                        update_stylesheet(index,url,prices,release_date,colorway,retail_price)

def run_all():
    data = read_data()
    proxy_ip_port = choose_proxy(proxy_path)

    if proxy_ip_port != "":
        options = {
            'proxy': {
                'http': proxy_ip_port,
                'https': proxy_ip_port
            }
        }
        chrome_options  = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome('chromedriver.exe', seleniumwire_options=options,chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    itterate_shoes(data,driver)
    driver.quit()

while True:
    run_all()
    time.sleep(3600)
