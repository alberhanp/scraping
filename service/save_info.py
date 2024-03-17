from urllib.parse import urlparse

from service.web_metric_insight import WebMetricsInsight


class SaveInfo:
    def __init__(self, url, websites_db):
        self.url = url
        self.websites_db = websites_db

    async def save(self):
        try:

            with WebMetricsInsight(self.url) as wmi:
                wmi.get_global_rank()
                wmi.get_country_rank()
                wmi.get_category_rank()
                wmi.get_total_visits()
                wmi.get_bounce_rate()
                wmi.get_pages_per_visit()
                wmi.get_visit_duration()

                parsed_url = urlparse(self.url)
                path = parsed_url.path
                website = path.split('website/')[-1]

                data = {
                    'Website': website,
                    'Global Rank': wmi.global_rank ,
                    'Country Rank': wmi.country_rank,
                    'Category Rank': wmi.category_rank,
                    'Total Visits': wmi.total_visits,
                    'Bounce Rate': wmi.bounce_rate,
                    'Pages per Visit': wmi.pages_per_visit,
                    'Average Visit Duration': wmi.avg_visit_duration
                }

                if self.websites_db.find_one_or_none({'Website': website}):
                    self.websites_db.update({'Website': website}, {'$set': data})
                else:
                    self.websites_db.insert(data)

        except Exception as e:
            raise e







