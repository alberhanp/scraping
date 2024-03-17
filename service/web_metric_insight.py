from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebMetricsInsight:
    def __init__(self, url):
        self.url = url
        self.initialize_driver()

        self.global_rank = None
        self.country_rank = None
        self.category_rank = None
        self.total_visits = None
        self.bounce_rate = None
        self.pages_per_visit = None
        self.avg_visit_duration = None
        self.gender_distribution = None

    def initialize_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

    def close_driver(self):
        self.driver.quit()

    def get_element_text(self, by, value, wait_time=10):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element.text.strip()
        except TimeoutException:
            print(f"Timeout waiting for element by {by} with value '{value}'")
            return None

    def get_global_rank(self):
        self.global_rank = self.get_element_text(By.CLASS_NAME,
                                                 'wa-rank-list__item--global .wa-rank-list__value') if self.get_element_text(
            By.CLASS_NAME, 'wa-rank-list__item--global .wa-rank-list__value') is not None else "Not Found"

    def get_country_rank(self):
        self.country_rank = self.get_element_text(By.CLASS_NAME,
                                                  'wa-rank-list__item--country .wa-rank-list__value') if self.get_element_text(
            By.CLASS_NAME, 'wa-rank-list__item--country .wa-rank-list__value') is not None else "Not Found"

    def get_category_rank(self):
        self.category_rank = self.get_element_text(By.CLASS_NAME,
                                                   'wa-rank-list__item--category .wa-rank-list__value') if self.get_element_text(
            By.CLASS_NAME, 'wa-rank-list__item--category .wa-rank-list__value') is not None else "Not Found"

    def get_total_visits(self):
        total_visits = self.get_element_text(By.XPATH,
                                             '//p[@data-test="total-visits"]/following-sibling::p[@class="engagement-list__item-value"]') if self.get_element_text(
            By.XPATH,
            '//p[@data-test="total-visits"]/following-sibling::p[@class="engagement-list__item-value"]') is not None else "Not Found"
        self.total_visits = total_visits if total_visits is not None else "Not Found"

    def get_bounce_rate(self):
        bounce_rate = self.get_element_text(By.XPATH,
                                            '//p[@data-test="bounce-rate"]/following-sibling::p[@class="engagement-list__item-value"]')
        self.bounce_rate = bounce_rate if bounce_rate is not None else "Not Found"

    def get_pages_per_visit(self):
        pages_per_visit = self.get_element_text(By.XPATH,
                                                '//p[@data-test="pages-per-visit"]/following-sibling::p[@class="engagement-list__item-value"]')
        self.pages_per_visit = pages_per_visit if pages_per_visit is not None else "Not Found"

    def get_visit_duration(self):
        avg_visit_duration = self.get_element_text(By.XPATH,
                                                   '//p[@data-test="avg-visit-duration"]/following-sibling::p[@class="engagement-list__item-value"]')
        self.avg_visit_duration = avg_visit_duration if avg_visit_duration is not None else "Not Found"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()
