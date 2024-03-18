from bson import ObjectId


def convert_objectid(obj):
    if obj is None:
        return None
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    if isinstance(obj, dict):
        return {key: str(value) if isinstance(value, ObjectId) else convert_objectid(value) for key, value in obj.items()}
    return obj


class GetInfo:
    def __init__(self, websites_db, url):
        self.website_db = websites_db
        self.url = url

    def get_info(self):
        try:
            result = self.website_db.find_one_or_none({'Website': self.url})
            if not result:
                return 'Nenhum dado encontrado para esse site.'
            return convert_objectid(result)

        except Exception as e:
            raise e

