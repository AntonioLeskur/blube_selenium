import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
import log_account


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# SAKRIJ CHROME:
# chrome_options.add_argument("--headless=new")

class Upload:

    def __init__(self):

        self.driver_blube = webdriver.Chrome(options=chrome_options)
        self.driver_blube.get("""
        https://blube.hr/administracija/catalog/product/
        index/key/05d4025d820049940680c5385f3c9f7fad3f3ef30f475749c7a90cc1f5187a92/
        """)

        username = log_account.user
        password = log_account.passw

        user_entry = self.driver_blube.find_element(By.NAME, value="login[username]")
        user_entry.send_keys(username)

        pass_entry = self.driver_blube.find_element(By.NAME, value="login[password]")
        pass_entry.send_keys(password)
        pass_entry.send_keys(Keys.ENTER)

    def start_upload(self, download_instance):

        wait = WebDriverWait(self.driver_blube, 40)
        wait.until(expected_conditions.visibility_of_element_located((By.ID, "search-global")))

        search = self.driver_blube.find_element(By.ID, value="search-global")
        self.product_name = download_instance.product_name_promo

        search.send_keys(download_instance.product_name_promo)

        wait.until(expected_conditions.element_to_be_clickable((By.ID, "searchPreviewProducts")))
        self.driver_blube.implicitly_wait(20)

        self.driver_blube.find_element(By.ID, value="searchPreviewProducts").click()

        wait.until(expected_conditions.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Configurable Product')]")))

        configurable = self.driver_blube.find_element(By.XPATH, value="//div[contains(text(), 'Configurable Product')]")
        configurable.click()

        # Go online
        wait.until(expected_conditions.presence_of_element_located((By.NAME,
                                                                    "product[status]")))

        checkbox = self.driver_blube.find_element(By.NAME, value="product[status]")
        if checkbox.is_selected():
            pass
        else:
            self.driver_blube.execute_script("arguments[0].click();", checkbox)

        time.sleep(2)

        wait.until(expected_conditions.presence_of_element_located((By.NAME, "product[weight]")))

        # Weight
        weight = self.try_to_upload_if(self.driver_blube.find_elements(By.NAME, value="product[weight]"))
        weight.send_keys(download_instance.weight)

        # Collapse Specifications
        wait.until(expected_conditions.presence_of_element_located\
                       ((By.XPATH, "//span[contains(text(), 'Specifications')]")))
        spec = self.driver_blube.find_element(By.XPATH, value="//span[contains(text(), 'Specifications')]")
        spec.click()

        self.driver_blube.implicitly_wait(20)

        # Dimensions
        dimensions = self.try_to_upload_if(self.driver_blube.find_elements(By.NAME, value="product[dimensions]"))
        dimensions.send_keys(download_instance.dimensions)

        # Box Dimensions
        box_dimensions = self.try_to_upload_if(self.driver_blube.find_elements(By.NAME, value="product[box_dimensions]"))
        box_dimensions.send_keys(download_instance.box_dimensions)


        # Packaging
        packaging = self.try_to_upload_if(self.driver_blube.find_elements(By.NAME, value="product[packaging]"))
        packaging.send_keys(download_instance.packaging)

        # Min Packaging
        min_packaging = self.try_to_upload_if(self.driver_blube.find_elements(By.NAME, value="product[package_qty]"))
        min_packaging.send_keys(download_instance.min_packaging)


        # Collapse Content
        content = self.driver_blube.find_element(By.XPATH, value="//strong[@class='admin__collapsible-title']/span")
        content.click()
        self.driver_blube.implicitly_wait(20)


        # Long Description
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "toggleproduct_form_description")))

        button_long = self.driver_blube.find_element(By.ID, value="toggleproduct_form_description")

        button_long.click()

        wait.until(expected_conditions.presence_of_element_located((By.ID, "product_form_description")))

        long_description = self.driver_blube.find_element\
            (By.ID, value="product_form_description")

        self.driver_blube.execute_script("arguments[0].style.visibility = 'visible';", long_description)

        long_description.clear()
        long_description.send_keys(download_instance.long_description)


        # Short Description
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "toggleproduct_form_short_description")))

        button = self.driver_blube.find_element(By.ID, value="toggleproduct_form_short_description")

        button.click()


        wait.until(expected_conditions.presence_of_element_located((By.ID, "product_form_short_description")))

        short_description = self.driver_blube.find_element\
        (By.ID, value="product_form_short_description")

        self.driver_blube.execute_script("arguments[0].style.visibility = 'visible';", short_description)

        self.driver_blube.implicitly_wait(20)

        short_description.clear()
        short_description.send_keys(download_instance.short_description)

        self.driver_blube.execute_script("window.scrollTo(0, 0);")
    def save_t(self):
        try:
            self.save_and_close_element = self.driver_blube.find_element(By.ID, "save-button")
            self.save_and_close_element.click()
            save_and_close_fin = self.driver_blube.find_element(By.ID, "save-button")
            save_and_close_fin.click()
        except StaleElementReferenceException:
            pass


    def save_and_close(self):
        import threading
        t_label = threading.Thread(target=self.save_t, daemon=True)
        t_label.start()



    @staticmethod
    def try_to_upload_if(element_selection):
        if len(element_selection) > 0:
            element = element_selection[0]
            if len(element.get_attribute("value")) > 0:
                element.clear()
                return element
            else:
                return element
        else:
            pass
