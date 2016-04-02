from selenium import webdriver


my_driver = webdriver.Chrome()
my_driver.get('http://www.google.com')
my_driver.find_element_by_id()