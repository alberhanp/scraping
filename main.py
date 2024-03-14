from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests

from repository.mongo_client import get_connection, DocumentDBClient

app = FastAPI()

mongo_client = DocumentDBClient(get_connection(), 'mensagens_enviadas')

# Function to simulate scraping data from SimilarWeb
# DISCLAIMER: This is not official and might not work


def scrap_similarweb(url: str):
    try:
        # Simulate sending a request to SimilarWeb (replace with actual API call if available)
        similar_url = f'https://www.similarweb.com/website/{url}/#overview'

        response = requests.get(similar_url, headers={'User-Agent': 'My Research Script'})
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sample logic to extract data (modify selectors as needed)
        rank = soup.find('div', class_='rank-value').text.strip()
        website = url
        category = soup.find('span', class_='category-name').text.strip()
        # Implement logic to find additional data as needed
        rank_change = None
        avg_visit_duration = None
        pages_per_visit = None
        bounce_rate = None
        top_countries = None
        gender_distribution = None
        age_distribution = None

        data = {
            'Rank': rank,
            'Website': website,
            'Category': category,
            'Rank Change': rank_change,
            'Average Visit Duration': avg_visit_duration,
            'Pages per Visit': pages_per_visit,
            'Bounce Rate': bounce_rate,
            'Top Countries': top_countries,
            'Gender Distribution': gender_distribution,
            'Age Distribution': age_distribution
        }
        return data
    except Exception as e:
        print(f"Error scraping data for {url}: {e}")
        return None


@app.get("/scrape/{url}")
def scrape(url: str):
    data = scrap_similarweb(url)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="Data could not be scraped")


if __name__ == '__main__':
    scrap_similarweb('google.com')

