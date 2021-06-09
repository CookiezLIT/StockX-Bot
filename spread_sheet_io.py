import time
from selenium import webdriver
from selenium_bot import get_details, perform_search
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

##shoe size charts:
#the tables are written from the nike shoe conversion site,
#make changes here if there are problems with size conversions
kids_us = [2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,1,1.5]
kids_eu = [17,19,18.5,19,19.5,20,21,21.5,22,22.5,23,24,24,25.5,26,26.5,27,27.5,28,28.5,29.5,30,31,31.5,32,33]
kids_uk = [1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,1]

men_us = [3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
men_uk = [3,3.5,4,4.5,5,5.5,6,6,6.5,7,7.5,8,8.5,0,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15]
men_eu = [35.5,36,36.5,37.5,38,38.5,39,40,40.5,41,42,42.5,43,44,44.5,45,45.5,46,47,47.5,48,48.5,49,49.5,50,50.5]

women_us = [4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5]
women_uk = [1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,0,9.5,10]
women_eu = [34.5,35,35.5,36,36.5,37.5,38,38.5,39,40,40.5,41,42,42.5,43,44,44.5,45]




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




def size_auxilliray(size):
    '''gets the size as string and returns the number'''
    number = 0
    for i in size:
        if i.isdigit():
            number = number * 10 + int(i)
        elif i == '.':
            number = number + 0.5
            return number
    return number

def convert_currency(price):
    number = 0
    for i in price:
        if i.isdigit():
            number = number * 10 + int(i)
    return number * 0.71



def calculate_size(size,type):
    if type == 'Kids':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = kids_eu.index(number)
                us_size = 'US ' + str(kids_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = kids_uk.index(number)
                us_size = 'US ' + str(kids_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    elif type == 'Mens':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = men_eu.index(number)
                us_size = 'US ' + str(men_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = men_uk.index(number)
                us_size = 'US ' + str(men_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    elif type == 'Womens':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = women_eu.index(number)
                us_size = 'US ' + str(women_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = women_uk.index(number)
                us_size = 'US ' + str(women_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    else:
        print('INVALID SHOE SIZE!')

def update_stylesheet(index, url,prices,release_date,colorway,retail_price):
    prices[0] = convert_currency(prices[0])
    prices[1] = convert_currency(prices[1])
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
                    shoe_name = perform_search(driver,search_url)
                    if shoe_name == "":
                        pass
                        print(style,"not found on stockx")
                    else:
                        url = generate_url(shoe_name)
                        type = row['Type']
                        size = calculate_size(row['Size'],type)

                        (prices, style, colorway, retail_price, release_date, ok) = get_details(driver, url, size)
                        if prices == []:  # preventing stockx 404 bug
                            pass
                        else:
                            if ok == True:
                                update_stylesheet(index,url,prices,release_date,colorway,retail_price)
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
    driver = webdriver.Chrome('chromedriver.exe')
    #driver = webdriver.Firefox()
    driver.maximize_window()
    itterate_shoes(data,driver)
    driver.quit()

while True:
    time.sleep(3600)
    run_all()