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
    time.sleep(0.51)
    #driver.find_element_by_id('menu-button-47').click()
    #driver.find_elements_by_class_name('chakra-menu__menu-button').click()
    #driver.find_element_by_xpath("//*[@data-testid='product-size-select']").click()
    #driver.find_element_by_class_name('css-amb8c0').click()
    #driver.find_element_by_class_name('select-control').click()
    try:
        driver.find_element_by_xpath('//button[contains(@id,"menu-button")]').click()
    except Exception:
        #print("ok")
        pass

    #click select size and then clicks the desired size
    time.sleep(0.5)
    #x = driver.find_elements_by_xpath("//*[contains(text(), 'us 7')]")
    x = driver.find_elements_by_class_name('css-8atqhb')


    for i in x:
        text = i.text
        if size in text:
            i.click()

    price_list = driver.find_elements_by_class_name('css-k008qs')
    prices = []
    for item in price_list:
        if '$' in item.text:
            prices.append(item.text)

    #print(prices)

    style = ""
    colorway = ""
    retail_price = ""
    release_date = ""
    try:
        style_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-style']")
        style = style_element.text
    except Exception:
        pass


    try:
        colorway_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-colorway']")
        colorway = colorway_element.text
    except Exception:
        pass

    try:
        retail_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-retail price']")
        retail_price = retail_element.text
        #print(retail_price)
    except Exception:
        pass

    try:
        release_element = driver.find_element_by_xpath("//*[@data-testid='product-detail-release date']")
        release_date = release_element.text
        #print(release_date)

    except Exception:
        pass
    #driver.quit()
    #print(prices)
    return (prices, style, colorway, retail_price, release_date)


#get_details(url2,'US 8')


