from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_page_data_mass(urls):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    data = []
    # browser.implicitly_wait(10)

    for url in urls:
        browser.get(url)
        try:
            sold = browser.find_element_by_class_name('j-orders-count').text
        except:
            sold = 0
        id = browser.find_element_by_class_name('j-article').text
        name = browser.find_element_by_class_name('name').text
        brand = browser.find_element_by_class_name('brand').text
        try:
            price_current = browser.find_element_by_class_name('final-cost').text
        except:
            price_current = ''
        try:
            price_prev = browser.find_element_by_class_name('c-text-base').text
        except:
            price_prev = ''
        try:
            color = browser.find_element_by_class_name('color').text
        except:
            color = ''
        try:
            rating = browser.find_element_by_class_name('product-rating').text
        except:
            rating = 0
        try:
            reviews = browser.find_element_by_xpath('//*[@id="comments_reviews_link"]/span/i').text
        except:
            reviews = 0

        # print(id, name, brand, sold, price_current, price_prev, rating, reviews, color)



        row = {'id': id,
                'name': name,
                'url': url,
                'brand': brand,
                'sold': sold,
                'price_current': price_current,
                'price_prev': price_prev,
                'rating': rating,
                'reviews': reviews,
                'color': color}
        data.append(row)
        print(row)

    browser.quit()
    return data

def get_page_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    data = []
    # browser.implicitly_wait(10)

    browser.get(url)
    try:
        sold = browser.find_element_by_class_name('j-orders-count').text
        sold = re.search(r'\d.+\d', sold).group(0)
        sold = sold.replace(' ','')
    except:
        sold = 0
    art = browser.find_element_by_class_name('j-article').text
    name = browser.find_element_by_class_name('name').text
    brand = browser.find_element_by_class_name('brand').text
    try:
        price_current = browser.find_element_by_class_name('final-cost').text
        price_current = re.search(r'\d.+\d', price_current).group(0)
        price_current = price_current.replace(' ','')
    except:
        price_current = ''
    try:
        price_prev = browser.find_element_by_class_name('c-text-base').text
        price_prev = re.search(r'\d.+\d', price_prev).group(0)
        price_prev = price_prev.replace(' ','')
    except:
        price_prev = ''
    try:
        color = browser.find_element_by_class_name('color').text
    except:
        color = ''
    try:
        rating = browser.find_element_by_class_name('product-rating').text
    except:
        rating = 0
    try:
        reviews = browser.find_element_by_xpath('//*[@id="comments_reviews_link"]/span/i').text
    except:
        reviews = 0
    try:
        browser.find_element_by_class_name('sort_select j-show-feedback').click()
        first_review = browser.find_element_by_xpath('//*[@id="Comments"]/div/div[3]/div[2]/div[1]/div[2]').get_attribute('content')
        print(first_review)
    except:
        first_review = ''

    # print(id, name, brand, sold, price_current, price_prev, rating, reviews, color)

    row = {'art': art,
           'name': name,
           'url': url,
           'brand': brand,
           'sold': sold,
           'price_current': price_current,
           'price_prev': price_prev,
           'rating': rating,
           'reviews': reviews,
           'color': color,
           'first_review': first_review}
    data.append(row)
    print(row)

    browser.quit()
    return data

def main():
    get_page_data('https://www.wildberries.ru/catalog/8016923/detail.aspx?targetUrl=ES')

if __name__ == '__main__':
    main()
