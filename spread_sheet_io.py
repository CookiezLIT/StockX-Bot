import time
from selenium import webdriver
from selenium_bot import get_details
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account


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
generate_url('Nike Dunk Low UNC (2021)')

data = read_data()


def calculate_size(size):

    if "UK" in size: #UK size:
        number = filter(str.isdigit, size)
        number = "".join(number)
        number = int(number)
        inches = int(number + 23 / 3)
        us_size = 3 * inches - 22
        size = "US " + str(us_size)
        return size

    elif "US" in size: #US size
        return size

    elif "EU" in size: #EU size:
        number = filter(str.isdigit, size)
        number = "".join(number)
        number = int(number)
        uk_size = int((number - 2) / 1.27) + 23
        us_size = uk_size + 1
        size = "US " + str(us_size)
        return size


driver = webdriver.Firefox()


for index, row in data.iterrows():
    #driver.get('https://www.google.com/')
    # BUYURL!!!!!!
    if row['Stock X URL'] == "":
        if (row['Shoe Name'] != ""):
            size = row['Size']
            size = calculate_size(size)

            url = generate_url(row['Shoe Name'])
            (prices, style, colorway, retail_price, release_date) = get_details(driver, url,size)
            if prices == []: #preventing stockx 404 bug
                pass
            else:
                target_sheet.update_cell(index+2,5,url)
                target_sheet.update_cell(index+2,3,prices[0])
                target_sheet.update_cell(index+2,4,prices[1])
                target_sheet.update_cell(index+2,7,release_date)
                target_sheet.update_cell(index+2,8,colorway)
                target_sheet.update_cell(index+2,9,retail_price)
                print(f"{row['Shoe Name']} :updated URL and done!")
    else:
        url = row['Stock X URL']
        size = row['Size']
        #check for size problems!!

        (prices, style, colorway, retail_price, release_date) = get_details(driver, url, size)
        if prices == []: #preventing stockx 404 bug
            pass
        else:
            target_sheet.update_cell(index + 2, 5, url)
            target_sheet.update_cell(index + 2, 3, prices[0])
            target_sheet.update_cell(index + 2, 4, prices[1])
            target_sheet.update_cell(index + 2, 7, release_date)
            target_sheet.update_cell(index + 2, 8, colorway)
            target_sheet.update_cell(index + 2, 9, retail_price)
driver.quit()