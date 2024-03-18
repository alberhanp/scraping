import time
from random import choice
import requests
import random

from bs4 import BeautifulSoup

from service.scraping_soup import ScrapingSoup


class SaveInfo:
    def __init__(self, url, websites_db):
        self.url = url
        self.websites_db = websites_db

    async def scrap_similarweb(self):
        try:
            response = self.fetch_with_curl()

            soup = BeautifulSoup(response, 'html.parser')

            scraping_soup = ScrapingSoup(soup)

            scraping_soup.get_global_rank()
            scraping_soup.get_country_rank()
            scraping_soup.get_category_rank()
            scraping_soup.get_total_visits()
            scraping_soup.get_bounce_rate()
            scraping_soup.get_pages_per_visit()
            scraping_soup.get_visit_duration()
            scraping_soup.get_gender_distribution()
            scraping_soup.get_mkt_channels_distribution()

            data = {
                'Website': self.url,
                'Global Rank: ': scraping_soup.global_rank,
                'Country Rank: ': scraping_soup.country_rank,
                'Category Rank: ': scraping_soup.category_rank,
                'Total Visits: ': scraping_soup.total_visits,
                'Bounce Rate: ': scraping_soup.bounce_rate,
                'Pages per Visit: ': scraping_soup.pages_per_visit,
                'Visit Duration: ': scraping_soup.avg_visit_duration,
                'Gender Distribution': scraping_soup.gender_distribution,
                'Marketing Channels Distribution': scraping_soup.mkt_channels_distribution
            }

            if self.websites_db.find_one_or_none({'Website': self.url}):
                self.websites_db.update({'Website': self.url}, {'$set': data})
            else:
                self.websites_db.insert(data)

        except Exception as e:
            print(f"Error scraping data: {e}")
            return None

    def fetch_with_curl(self):
        # Funcionou com esses user agents, não senti necessidade de inserir mais, mas se precisar, é só adicionar.
        user_agents = [
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
            "Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
            "Mozilla/5.0 (Linux; Android 12; moto g stylus 5G (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; moto g pure) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        ]

        url_get_cookies = 'https://www.similarweb.com/'
        headers_get_cookies = {
            'authority': 'www.similarweb.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'same-site': 'None',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': choice(user_agents),
        }

        # Estava funcionando sem proxy, mas depois de um tempo, começou a dar erro 403, então adicionei um proxy.
        # Achei esses proxies na internet, não sei se são os melhores, mas funcionaram (todos BR).

        proxies_list = [
            'http://52.67.10.183:3128',
            'http://52.67.10.183:80',
            'http://54.233.119.172:3128',
            'http://18.228.198.164:80',
            'http://20.206.106.192:8123',
            'http://20.206.106.192:80',
            'http://20.206.106.192:80'
        ]

        proxy = {
            'http': choice(proxies_list),
        }

        sessao = requests.Session()
        request_get_cookies = sessao.get(url_get_cookies,
                                         headers=headers_get_cookies, proxies=proxy)

        if request_get_cookies.ok:
            tempo_espera = random.uniform(6,
                                          13)  # Coloquei um tempo de espera para simular um comportamento mais humano, antes tava conseguindo só 2 requisições
            time.sleep(tempo_espera)

            headers_get_data = {

                # Tirei esses headers do navegador, mas não sei se são todos necessários, mantive pra simular melhor o navegador (e tbm pq funcionu assim :p)

                'authority': 'www.similarweb.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                          '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'pt-BR,pt;q=0.9',
                'cache-control': 'no-cache',
                'dnt': '1',
                'x-requested-with': 'XMLHttpRequest',
                'same-site': 'None',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': choice(user_agents),
                'referer': 'https://www.similarweb.com/',
            }

            proxy2 = {
                'http': choice(proxies_list),
            }

            url_get_data = f'https://www.similarweb.com/website/{self.url}/'
            resposta_get_data = sessao.get(url_get_data,
                                           headers=headers_get_data, proxies=proxy2)

            resposta_em_texto = resposta_get_data.text

            return resposta_em_texto
