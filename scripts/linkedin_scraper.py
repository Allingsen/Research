from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

'''DEPRECEATED. NO LONGER PART OF THIS PROJECT'''
class Scraper():
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        #self.EMAIL = 'alexcellingsen@gmail.com'
        #self.PASSWORD = '8PdLbErC7gY#6f/'
        self.linked_soup = None

    def get_post(self, post: str) -> list:
        '''Gets the text of the post from a given webpage'''
        # Access the webpage, sleeps to allow proper loading
        self.driver.get(post)
        time.sleep(5)

        # Grabs the HTML
        html_page = self.driver.page_source
        self.linked_soup = BeautifulSoup(html_page.encode('utf-8'), 'html')
        
        # Finds the JSON of the correct element
        text = self.linked_soup.find_all('script', {'type' : 'application/ld+json'})
        texts = []
        
        # Gets the text of the post and adds to the list of texts
        for i in text:
            str_post = str(i)[35:-10]   # Removes the tag headlines and makes them a JSON
            json_post = json.loads(str_post)
            texts.append(json_post['articleBody'])

        return texts
    
    def get_comments(self, post) -> list:
        '''Gets the text of comments on a given LinkedIn post'''
        self.driver.get(post)
        x = self.driver.find_element(By.CLASS_NAME, '''comments-comment-entity
        
        ''')
        print(x)


scraper = Scraper()
#print(scraper.get_post('https://www.linkedin.com/posts/onxmaps_corporate-development-associate-remote-considered-activity-7221197367348228096-ghVc/?utm_source=share&utm_medium=member_desktop'))
scraper.get_comments('https://www.linkedin.com/posts/onxmaps_corporate-development-associate-remote-considered-activity-7221197367348228096-ghVc/?utm_source=share&utm_medium=member_desktop')