from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# SAKRIJ CHROME:
# chrome_options.add_argument("--headless=new")

class Download:

    def __init__(self):

        self.driver_promobox = webdriver.Chrome(options=chrome_options)
        self.driver_promobox.get("https://promobox.com/hr/")
        self.product_name_promo = ""
        self.image_source = ""
        self.weight = ""
        self.dimensions = ""
        self.box_dimensions = ""
        self.packaging = ""
        self.min_packaging = ""
        self.short_description = ""
        self.long_description = ""

    def start_download(self, product):

        search = self.driver_promobox.find_element(By.NAME, value="phrase")
        search.send_keys(product)
        search.send_keys(Keys.ENTER)
        wait = WebDriverWait(self.driver_promobox, 10)
        selection = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".card-title")))
        self.product_name_promo = selection.text
        selection.click()

        self.picture_element = self.driver_promobox.find_element(By.CSS_SELECTOR, "picture.d-block.img-fluid")
        self.img_element = self.picture_element.find_element(By.TAG_NAME, "img")
        self.image_source = self.img_element.get_attribute("src")

        wait.until(expected_conditions.presence_of_element_located((By.ID, "ajax-netow")))
        self.weight = self.driver_promobox.find_element(By.ID, value="ajax-netow").text
        self.dimensions = self.try_to_find(self.driver_promobox.find_elements\
            (By.XPATH, value="//td[contains(text(), 'Dimenzija')]/following-sibling::td"))
        self.box_dimensions = self.try_to_find(self.driver_promobox.find_elements(By.ID, value="ajax-cdimensions"))
        self.packaging = self.try_to_find(self.driver_promobox.find_elements(By.ID, value="ajax-pakow"))
        self.min_packaging = self.packaging_split(self.packaging)

        self.short_description = self.try_to_find(self.driver_promobox.find_elements\
                (By.XPATH, value="//div[@class='dg2-model-naslov mb-4']/h1")).split("-")[1]

        self.long_description = self.try_to_find(self.driver_promobox.find_elements\
            (By.XPATH, value="//td[contains(text(), 'Opis')]/following-sibling::td"))


    @staticmethod
    def try_to_find(element_selection):
        if len(element_selection) > 0:
            return element_selection[0].text
        else:
            return ""
    @staticmethod
    def packaging_split(data):
        if "/" in data:
            return data.split("/")[1]
        else:
            return data
