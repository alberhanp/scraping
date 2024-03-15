import subprocess

from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from uuid import uuid4

from repository.mongo_client import get_connection, DocumentDBClient

app = FastAPI()

mongo_client = DocumentDBClient(get_connection(), 'scraping_similarweb')


def scrap_similarweb(url: str):
    try:
        # Simulate sending a request to SimilarWeb (replace with actual API call if available)

        response = fetch_with_curl(url)
        soup = BeautifulSoup(response, 'html.parser')

        value_element = soup.find('p', class_='wa-rank-list__value')

        if value_element:
            # Extraindo e limpando o número
            rank_number = value_element.text.replace('#', '').strip()
            print(rank_number)

        # # Sample logic to extract data (modify selectors as needed)
        # rank = soup.find('div', class_='"wa-rank-list__value"').text.strip()
        # website = soup.find('h1', class_='websiteHeader-title').text.strip()
        # category = soup.find('span', class_='category-name').text.strip()
        # # Implement logic to find additional data as needed
        # rank_change = None
        # avg_visit_duration = None
        # pages_per_visit = None
        # bounce_rate = None
        # top_countries = None
        # gender_distribution = None
        # age_distribution = None
        #
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

    sg_id = str(uuid4())
    curl_command = f"""
curl 'https://www.similarweb.com/website/{url}/' \
  -H 'authority: www.similarweb.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: pt-BR,pt;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'cookie: bm_sz=EF71AB4F0075ACDA28B7B3012C1DC946~YAAQhwkTAuYizjaOAQAAnZPHPxdQ0V5e8XIJ+va0PcyncRtJtPaHNiN/TefRIsnHXLnmy+HftlzL5ly0edLHX+sSWZlX/8Kj30we3zfINoXbVdYH7NQVt8WNlyPlf5xsI1kHHm8isDJwdzwQPCOnGOXL0sxoahEQ7M7p3KwuySHYTqJU8tZEaIepy6nlZtaClrU/uCwXUxaZ+yIoRDP0jtXTWm5U4JeWw4bQK8G2tZUP7IOZvD2QEjOOT1/4t6jVJAeY/nDxVT4zj7BfkDn6UtZOSqfXkgd3x+rOFe7NO8BbJ9Dv8Fas5xkOTrijQhHI686vvlSlYDM0WT3ofOw6cOcq5Q2WBAnhHbQgLuFk4qSTxuh+TaG8U3IWkEo=~4340022~3163206; sgID={sg_id}; bm_mi=F2BB4EEF689E327DC2527E7A2893358A~YAAQhwkTAvkizjaOAQAANKTHPxf6EyEAevuSOnqYT/rWfTGxvvcJvHIDXyMLdO98YzicrZZH7AwsjM4v332knnQ6AiKjRZulOfqYbx3lbgp81ypWjb7nS3zf3l3u7VGZdGNCvG6pW07LdOvSiHmyAIoF7eIq0dXRqyMVs5/TCH6qhW1P5i+fyaEpHjThZpdPPKPGClxTLG+v9PslbRD0YVrMV/rUVzGmyZKcDisU0vdIHa4IP7Z0U+H0PsUb2TKwuxdXC+xYUzZ3q9onQvJqnMehT6XFRQLBGrDUgjVGaa5eOWQH/zrYD7C2UONdPLeMJo3eK86Qf9SNKgNN6NU40evGVw==~1; fsrndid=false; _gcl_au=1.1.2090925423.1710467033; _gid=GA1.2.276102734.1710467033; ak_bmsc=A1A95B42FBC98F7C35D74C2E4BD1C709~000000000000000000000000000000~YAAQhwkTAgAjzjaOAQAA2afHPxepbvsHbrJEKSwyATWVxYN3cQr6897t4RXeu4K2Uhb8BqxOpDjlfFY7MJDpaxXcQqfkhYBR37rcOmpJa4KLAkq/a4wW/TJidV12x1tAIbOmY4oLW20kdjjh/mWpH7nPvClz7CYm5F++PhGyhnR3vkGmts7BhAVBl3qzksBZyxZa8F5NEKeRXt3nr8BUT/2Of8/Z+3ewYIY/hIM6Zl3Z1o3aOYnNgnH9wYgqlpEQyJHt0QhfLwPHQasKnbSNtjFdUDLQSen0HdKS+CZxXEmiGlA02lrgtXSN6jkRXfHg4h7Y5QeSxihKl3Kx+maNV/LaVJJd/sv1RpPmMl14yRHztWUOzEyeJjpB1w+n+PyjLcC6poakblgQOC7rrE9txddmdttg1VYHS9+AZQ1iAYt/Ptaj5q2eJKXOCtg/XhcFgJSWn8opQ1gmxJnNaSuwWA5bks3L2/2YTiPQvVJ9IoiCjcdru854aHXM497YizT79EvihZ8=; _pk_id.1.fd33=858f066f0e25e937.1710467033.; _abck=8450BB03449AB666A4773F8648C5EB16~0~YAAQhwkTAgEjzjaOAQAADL7HPwviKFx9sKI5dX/bVrkjio9XlnaYL9i+oLfLATwabhhlTXj/5Iy3IlqPzmI9HrvB/piwRBf5lmMuyzoc5ltRpPbCZQmXy15UGbCDll1wKrccdGzISUxOD0tVA3M4ysK+ZXb6k/llfJF2tkTIwdtTp2qqi2kcpeEWAwE1YqNOBQLcFo7aiw90wDntoujaQgz1pJSRbNtwE2JuZXDQLi7UaA2Lkbv09CmCxPc2OSUBMEWWGxph7oiqqOd4gq+HHejA1h5b6xmFPtn+tOzfId17sh3NEl0rxDHEbN1/ZEdPJlRS7EOpbVeg/a03EUyn6H1zjU8e2+pdl6riZl1wUNC6x8sCs0r95anUvqYmnA4w/f5xj6vB3BW0XHcqQlg3IWLCjxdjfEYs8qsD~-1~-1~-1; _clck=1k1m8s8%7C2%7Cfk3%7C0%7C1535; OptanonAlertBoxClosed=2024-03-15T02:17:16.823Z; _pk_ses.1.fd33=1; loyal-user={{%22date%22:%222024-03-15T01:43:53.028Z%22%2C%22isLoyal%22:true}}; dicbo_id=%7B%22dicbo_fetch%22%3A1710469037617%7D; bm_sv=3ABAF7EE53E56BB4E0CF11038988568F~YAAQsQkTAqkzDjyOAQAAKR7nPxcqU93HMz5nhC+L7Grlc0mluoNH/swtRlgeeLGb6550sqWnTYylH6fCQOOD4Poxjxfokfp3C/ogLAFImKjQh6s4+o3Gf0y0HgMUoQLUMILlk76Ho4az83bOiT4ahSbCtWxgsX3c1xmDNhk/ngOyJEQF4LYd9MiHTlqWe0U1W8aHk6nI+4Q0Mgt0yooE2WiMCOtVHdYp2GBu3bGbFvv1xrnYqL805qfe76l18njYl3a+PG0=~1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+14+2024+23%3A18%3A15+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=cc5fd1c1-71ff-4ab1-938c-56940a0875d5&interactionCount=2&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=BR%3BMG; _ga=GA1.1.651739860.1710467033; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18e3fc7c239842-0c1afb241799e1-1e462c6c-1fa400-18e3fc7c239842%22%2C%22%24device_id%22%3A%20%2218e3fc7c239842-0c1afb241799e1-1e462c6c-1fa400-18e3fc7c239842%22%2C%22sgId%22%3A%20%22e42c6fc9-0683-4b83-bace-0a939ba66b47%22%2C%22site_type%22%3A%20%22lite%22%2C%22session_id%22%3A%20%226c4d3871-0142-4fa2-8644-9ceb962f1629%22%2C%22session_first_event_time%22%3A%20%222024-03-15T02%3A17%3A17.233Z%22%2C%22url%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Ffacebook.com%2F%22%2C%22language%22%3A%20%22en-us%22%2C%22section%22%3A%20%22website%22%2C%22sub_section%22%3A%20%22%22%2C%22sub_sub_section%22%3A%20%22%22%2C%22sw_extention%22%3A%20false%2C%22last_event_time%22%3A%201710469095745%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Fgoogle.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.similarweb.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Fgoogle.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.similarweb.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22is_sw_user%22%3A%20false%2C%22entity_id%22%3A%20%22facebook.com%22%2C%22entity_name%22%3A%20%22facebook.com%22%2C%22main_category%22%3A%20%22computers_electronics_and_technology%22%2C%22sub_category%22%3A%20%22social_networks_and_online_communities%22%2C%22mode%22%3A%20%22single%22%2C%22ga_connection%22%3A%20%22not%20connected%22%2C%22limit_pop_up%22%3A%20false%2C%22first_time_visitor%22%3A%20false%2C%22cookies%22%3A%20%22accepted%22%7D; _uetsid=7e9bb4c0e26d11ee926dd9a4e25c09ac; _uetvid=7e9bf9a0e26d11eeb139372e0bf3ad94; _clsk=o3e273%7C1710469096988%7C5%7C1%7Cj.clarity.ms%2Fcollect; __q_state_9u7uiM39FyWVMWQF=eyJ1dWlkIjoiYjIwZmYzN2QtOGNmOS00NTkyLTljOGYtOTE1YzIyNDdkYjlkIiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJtZXNzZW5nZXJFeHBhbmRlZCI6ZmFsc2UsInByb21wdERpc21pc3NlZCI6ZmFsc2UsImNvbnZlcnNhdGlvbklkIjoiMTM1MzM2MDE2ODY3ODI4NjQ5OSJ9; RT="z=1&dm=www.similarweb.com&si=17c3dc6e-3654-4d61-a351-af901b8c6324&ss=ltrzwlgw&sl=4&tt=22b&obo=2&rl=1&ld=18wlq&r=3brc7i34&ul=18wlr&hd=18wls"; _ga_V5DSP51YD0=GS1.1.1710469037.2.1.1710469123.60.0.0' \
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
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
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
    scrap_similarweb('casasbahia.com.br')
