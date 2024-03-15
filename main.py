import subprocess
from datetime import datetime

from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from uuid import uuid4

from repository.mongo_client import get_connection, DocumentDBClient
from service.web_metric_insight import WebMetricsInsight

app = FastAPI()

mongo_client = DocumentDBClient(get_connection(), 'scraping_similarweb')


def scrap_similarweb(url: str):
    try:
        response = fetch_with_curl(url)

        soup = BeautifulSoup(response, 'html.parser')

        web_metrics = WebMetricsInsight(soup)

        web_metrics.get_global_rank()
        web_metrics.get_country_rank()
        web_metrics.get_category_rank()
        web_metrics.get_total_visits()
        web_metrics.get_bounce_rate()
        web_metrics.get_pages_per_visit()
        web_metrics.get_visit_duration()
        web_metrics.get_gender_distribution()

        print(f'Global Rank: {web_metrics.global_rank}')
        print(f'Country Rank: {web_metrics.country_rank}')
        print(f'Category Rank: {web_metrics.category_rank}')
        print(f'Total Visits: {web_metrics.total_visits}')
        print(f'Bounce Rate: {web_metrics.bounce_rate}')
        print(f'Pages per Visit: {web_metrics.pages_per_visit}')
        print(f'Average Visit Duration: {web_metrics.avg_visit_duration}')
        print(f'Gender Distribution: {web_metrics.gender_distribution}')

        # data = {
        #     'Rank': rank,
        #     'Website': website,
        #     'Category': category,
        #     'Rank Change': rank_change,
        #     'Average Visit Duration': avg_visit_duration,
        #     'Pages per Visit': pages_per_visit,
        #     'Bounce Rate': bounce_rate,
        #     'Top Countries': top_countries,
        #     'Gender Distribution': gender_distribution,
        #     'Age Distribution': age_distribution
        # }
        # return data
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None


@app.get("/scrape/{url}")
def scrape(url: str):
    data = scrap_similarweb(url)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="Data could not be scraped")


def fetch_with_curl(url: str):

    now = datetime.now()
    dt_now = now.isoformat(timespec='milliseconds')
    sg_id = str(uuid4())
    si = str(uuid4())

    curl_command = f"""
curl 'https://www.similarweb.com/website/{url}/' \
  -H 'authority: www.similarweb.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: pt-BR,pt;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'cookie: sgID={sg_id}; bm_sz=B515761369D61EE6FC2A1DB4776B1A3E~YAAQhwkTAuV3zjaOAQAAd+M1QxeJ2kCmm9cJEWFxKbQmrr7iemixjux2Yg2S8EHFqYlv76JQCV2beQcDUUGTzlePC31zcmK2n9S1jnSFWfhwtH2QM+E9ovNF8kCjKJvoQQn0i3/TMoGemHR36/RbjO6/fNVLxfnUEY4ThvF8LgSfFhpyzZW9/FcxmVoox6irAZQzTdF1/P8HMLZHVkg+IucPfvEIqM0VJ7afdBlUHiue230u+uDfC4vJ1OaaBqfGKAtnuOhBnaietUGMpqFm2OZ/SezAHTdRwwvcgfxlCigh5zKgnBznmq4unkdMOYP+/bTqdtEn3Z8Gkx2qPv5n5MU7z7/wxsUYmPUxdoPumjnuQ94szy5LABDgwSA=~3223859~3753281; _gcl_au=1.1.1664054494.1710524589; _gid=GA1.2.1099016975.1710524589; _pk_id.1.fd33=144dcb920cdf859e.1710524590.; OptanonAlertBoxClosed=2024-03-15T17:43:15.322Z; _clck=17hlbgs%7C2%7Cfk3%7C0%7C1535; _abck=2A8BB3137F3656EA6A0819AF8D5759C1~0~YAAQsQkTAvpiJzyOAQAASnVpQwsePvAFAZa245zES+no4Eqxbk+YZz4N87Dlpmrk49b7l/IXStvXux318oQ2l4ZWLnAdkk5sYQGcV9QL8o2l0+PpXVTMcbkv2CTpuCshOP4KZDy5Vy1quJ9h02hylVXoeReZLrGxhfALZ5tqo7DS5ABEQ5o6FenJxsY8poeSMjcGrpSE6ywsjG3ySX48JLEQ6qobpMirU/dT1SfH3VXdsJIheDhEGx8b1YDcuq4gZ7Hq9CNaHljkqvSVfQal5yWcod2ER4ueOd2on3bBXOhzEygCaCED9ZPUR8gykujyZ9DR5EueYIfuip/L+qafbihRkHMi7jv8K2y2CGo7vg4Xt8ACTYW2bdS5uYelzPj969yGY+ajWtNDFTrBadU0m+gEbXNVajXY7yxB~-1~-1~-1; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Mar+15+2024+15%3A39%3A29+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=00b9e4c7-6299-442f-abcc-2e0200e5f224&interactionCount=2&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=BR%3BMG; _ga_V5DSP51YD0=GS1.1.1710527966.2.1.1710527969.57.0.0; _ga=GA1.1.950981336.1710524589; _uetsid=8068a8f0e2f311eeb31be18e2d3d3743; _uetvid=80689510e2f311ee8d9f0b8f34dd783d; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18e4335fc5c1da-09f2c1733d615d-1e462c6c-1fa400-18e4335fc5d1da%22%2C%22%24device_id%22%3A%20%2218e4335fc5c1da-09f2c1733d615d-1e462c6c-1fa400-18e4335fc5d1da%22%2C%22sgId%22%3A%20%22{sg_id}%22%2C%22site_type%22%3A%20%22lite%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22session_id%22%3A%20%2281de6102-d25b-4dfd-aa33-f2d7febd1da3%22%2C%22session_first_event_time%22%3A%20%222024-03-15T18%3A39%3A12.674Z%22%2C%22url%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2F{url}%2F%22%2C%22language%22%3A%20%22en-us%22%2C%22section%22%3A%20%22website%22%2C%22sub_section%22%3A%20%22%22%2C%22sub_sub_section%22%3A%20%22%22%2C%22sw_extention%22%3A%20false%2C%22last_event_time%22%3A%201710527969201%2C%22is_sw_user%22%3A%20false%2C%22entity_id%22%3A%20%22coca-cola.com%22%2C%22entity_name%22%3A%20%22coca-cola.com%22%2C%22main_category%22%3A%20%22food_and_drink%22%2C%22sub_category%22%3A%20%22beverages%22%2C%22mode%22%3A%20%22single%22%2C%22ga_connection%22%3A%20%22not%20connected%22%2C%22limit_pop_up%22%3A%20false%2C%22first_time_visitor%22%3A%20false%2C%22cookies%22%3A%20%22accepted%22%7D; loyal-user={{%22date%22:%22{dt_now}Z%22%2C%22isLoyal%22:true}}; __q_state_9u7uiM39FyWVMWQF=eyJ1dWlkIjoiYzk3OTg4OWItOGZkMi00MjU1LThhM2UtNDE0YmJiNDc1NTUzIiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJtZXNzZW5nZXJFeHBhbmRlZCI6ZmFsc2UsInByb21wdERpc21pc3NlZCI6dHJ1ZSwiY29udmVyc2F0aW9uSWQiOiIxMzUzODE0ODk4ODMwODY5NjQ4In0=; _clsk=1gks20p%7C1710532311471%7C6%7C1%7Cj.clarity.ms%2Fcollect; RT="z=1&dm=www.similarweb.com&si={si}&ss=ltt06qjb&sl=1&tt=0&obo=1&ld=2l6x2&ul=2l6x2"' \
  -H 'pragma: no-cache' \
  -H 'referer: https://www.similarweb.com/website/{url}/' \
  -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
  --compressed
    """
    try:
        result = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl: {e.stderr}")
        return None


if __name__ == '__main__':
    scrap_similarweb('coca-cola.com')
