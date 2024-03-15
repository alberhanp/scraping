class WebMetricsInsight:
    def __init__(self, soup):
        super().__init__()
        self.gender_distribution = None
        self.avg_visit_duration = None
        self.pages_per_visit = None
        self.bounce_rate = None
        self.soup = soup
        self.total_visits = None
        self.category_rank = None
        self.country_rank = None
        self.global_rank = None

    def get_global_rank(self):
        global_rank_div = self.soup.find('div', class_='wa-rank-list__item wa-rank-list__item--global')
        global_rank_value_p = global_rank_div.find('p', class_='wa-rank-list__value')
        self.global_rank = global_rank_value_p.text.strip()

    def get_country_rank(self):
        country_rank_div = self.soup.find('div', class_='wa-rank-list__item wa-rank-list__item--country')
        country_rank_value_p = country_rank_div.find('p', class_='wa-rank-list__value')
        self.country_rank = country_rank_value_p.text.strip()

    def get_category_rank(self):
        category_rank_div = self.soup.find('div', class_='wa-rank-list__item wa-rank-list__item--category')
        category_rank_value_p = category_rank_div.find('p', class_='wa-rank-list__value')
        self.category_rank = category_rank_value_p.text.strip()

    def get_total_visits(self):
        total_visits_name_p = self.soup.find('p', attrs={"data-test": "total-visits"})
        total_visits_value_p = total_visits_name_p.find_next('p', class_='engagement-list__item-value')
        self.total_visits = total_visits_value_p.text.strip()

    def get_bounce_rate(self):
        bounce_rate_name_p = self.soup.find('p', attrs={"data-test": "bounce-rate"})
        bounce_rate_value_p = bounce_rate_name_p.find_next('p', class_='engagement-list__item-value')
        self.bounce_rate = bounce_rate_value_p.text.strip()

    def get_pages_per_visit(self):
        pages_per_visit_name_p = self.soup.find('p', attrs={"data-test": "pages-per-visit"})
        pages_per_visit_value_p = pages_per_visit_name_p.find_next('p', class_='engagement-list__item-value')
        self.pages_per_visit = pages_per_visit_value_p.text.strip()

    def get_visit_duration(self):
        visit_duration_name_p = self.soup.find('p', attrs={"data-test": "avg-visit-duration"})
        visit_duration_value_p = visit_duration_name_p.find_next('p', class_='engagement-list__item-value')
        self.avg_visit_duration = visit_duration_value_p.text.strip()

    def get_gender_distribution(self):
        demographics = {}

        gender_items = self.soup.select('.wa-demographics__gender-legend-item')

        for item in gender_items:
            gender_title = item.find('span', class_='wa-demographics__gender-legend-item-title').text.strip()
            gender_value = item.find('span', class_='wa-demographics__gender-legend-item-value').text.strip()
            demographics[gender_title] = gender_value

        self.gender_distribution = demographics

#  cf1fd7a2-4387-4f78-be6f-de35d729da7c






