import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


def get_details(driver, url,size):
    '''
    :param url:link of the shoe format : 'https://stockx.com/air-jordan-1-retro-high-black-white-light-smoke-grey'
    :param size:shoe size: format 'US 10'
    :return: tuple : (prices, style, colorway, retail_price, release_date)
    '''
    print('Working on shoe:')
    print('URL:',url)
    print('Shoe size:',size)
    print('---------------------------------------')
    print('AQUIRED DATA:')
    driver.get(url)
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    #accept all the shit
    try:#this try except is because we might have loaded the website already for the previos pair
        driver.find_element_by_class_name('css-unzfas-button').click()
    except Exception:
        pass

    #print(driver.find_element_by_class_name('stats').find_element_by_xpath("//div[1]").text)

    ###improve?
    time.sleep(1.51)
    #driver.find_element_by_id('menu-button-35').click()
    #driver.find_elements_by_class_name('chakra-menu__menu-button').click()
    #driver.find_element_by_xpath("//*[@data-testid='product-size-select']").click()
    #driver.find_element_by_class_name('css-amb8c0').click()
    #driver.find_element_by_class_name('select-control').click()
    #driver.find_element_by_class_name('css-onkibi').click()

    #click the size selection button
    try:
        buttons = driver.find_elements_by_xpath('//button[contains(@id,"menu-button")]')
        for button in buttons:
            try:
                button.click()
            except Exception as e:
                pass
                #sometimes there are dumb hidden buttons with the same name
    except Exception as e:
        print(e)
        pass


    #click select size and then clicks the desired size
    time.sleep(1.5)
    #x = driver.find_elements_by_xpath("//*[contains(text(), 'us 7')]")
    x = driver.find_elements_by_class_name('css-8atqhb')

    #ok checks if the size is found or not
    ok = False
    for i in x:
        text = i.text
        if size in text:
            ok = True
            i.click()
            print('bine')
            break

    #find both prices
    price_list = driver.find_elements_by_class_name('css-k008qs')


    prices = []
    price1 = ""
    price2 = ""
    for item in price_list:
        if item.text != "":
            if price1 == "":
                price1 = item.text
            elif price2 == "":
                price2 = item.text


    if u"\xA3" not in price1:
    #if '€' not in price1:
        price1 = '0'
    if u"\xA3" not in price2:
    #if '€' not in price2:
        price2 = '0'


    prices = [price1, price2]
    print('Highest bid:',price1)
    print('Lowest ask:',price2)
    #finding other details for the shoe: style,colorway,retail_price,release_date
    style = ""
    colorway = ""
    retail_price = ""
    release_date = ""
    try:
        style_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-style']")
        style = style_element.text
        print('Style:', style)
    except Exception:
        pass


    try:
        colorway_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-colorway']")
        colorway = colorway_element.text
        print('Colorway',colorway)
    except Exception:
        pass

    try:
        retail_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-retail price']")
        retail_price = retail_element.text
        print('Retail price:',retail_price)
    except Exception:
        pass

    try:
        release_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-release date']")
        release_date = release_element.text
        print('Release date:',release_date)

    except Exception:
        pass
    #driver.quit()
    #print(prices)
    print('Working on shoe done!')
    print('---------------------------------------')
    print('---------------------------------------')
    return (prices, style, colorway, retail_price, release_date, ok)

def perform_search(driver,url):
    '''
    Performs the search and returns the first shoe that is found:
    can improve the formula

    :param driver: webdriver
    :param url: generated_url for the search
    :return: the shoe url
    '''
    driver.get(url)

    #accepting all the page shit
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    try:
        driver.find_element_by_class_name('css-unzfas-button').click()
    except Exception:
        pass
    element = ""
    time.sleep(2)#to make sure the search results have time to load, can increase this ammount if the internet connection is slow
    try:
        # element = driver.find_elements_by_class_name('e1inh05x0')[0]
        # return element.text
        search_item = driver.find_elements_by_class_name('e1yt6rrx0')[0]
        url_link = search_item.find_element_by_tag_name("a")
        print('Searched for a shoe, found this url:')
        print(url_link.get_attribute('href'))

        return url_link.get_attribute('href')
    except Exception:
        pass
        #element not found
        return ""



###TESTING
# url2 = 'https://stockx.com/nike-dunk-low-unc-2021-ps'
# driver = webdriver.Firefox()
# get_details(driver, url2,'US 12')


