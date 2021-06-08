from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time


chrome_driver_path = "D:\development\chromedriver.exe"
soup_link = "https://www.zillow.com/pittsburgh-pa/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Pittsburgh%2C%20PA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.23239418457034%2C%22east%22%3A-79.69269081542971%2C%22south%22%3A40.28475113492149%2C%22north%22%3A40.60799735973734%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A26529%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A306709%7D%2C%22mp%22%3A%7B%22max%22%3A1000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
sheet_url = "https://docs.google.com/forms/d/e/1FAIpQLSdH8zeMiYB7YdVk7jr__wC9w612y-ixXZZR4lKUbdrLQ7jggQ/viewform?usp=sf_link"


headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"
}


class ApartmentFinder:

    def __init__(self):
        self.links = []
        self.addresses = []
        self.prices = []
        self.manage_soup()

    def manage_soup(self):
        response = requests.get(soup_link, headers=headers)
        response_text = response.text
        soup = BeautifulSoup(markup=response_text, features="html.parser")
        cards = soup.find_all(name="div", class_="list-card-info")
        for card in cards:
            self.addresses.append(card.find(name="address", class_="list-card-addr").getText())
            self.prices.append(card.find(name="div", class_="list-card-price").getText())

        all_link_elements = soup.select(".list-card-top a")
        for link in all_link_elements:
            href = link["href"]
            self.links.append(href)

    def fill_out_forms(self):
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

        for i in range(len(self.links)):
            self.driver.get(sheet_url)
            time.sleep(2)
            addr = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            addr.send_keys(self.addresses[i])
            price = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price.send_keys(self.prices[i])
            link = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link.send_keys(self.links[i])
            submit = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
            submit.click()
            time.sleep(2)



finder = ApartmentFinder()
finder.fill_out_forms()