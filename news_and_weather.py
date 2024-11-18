import requests

class NewsAndWeather:
    def __init__(self, news_api_key, weather_api_key):
        self.news_api_key = news_api_key
        self.weather_api_key = weather_api_key
        self.news_url = "http://newsapi.org/v2/top-headlines"
        self.weather_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_news(self, country='us'):
        """Récupère les actualités principales pour un pays donné."""
        params = {
            'apiKey': self.news_api_key,
            'country': country,
            'pageSize': 2  # Limite à 5 articles
        }
        response = requests.get(self.news_url, params=params)
        print(response.status_code, response.text)  # Ajouter cette ligne pour debug
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [f"{article['title']} - {article['source']['name']}" for article in articles]
        else:
            return ["Erreur lors de la récupération des actualités."]

    def get_weather(self, city='Paris'):
        """Récupère les informations météo pour une ville donnée."""
        params = {
            'q': city,
            'appid': self.weather_api_key,
            'units': 'metric',
            'lang': 'fr'
        }
        response = requests.get(self.weather_url, params=params)
        if response.status_code == 200:
            data = response.json()
            description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"À {city}, il fait actuellement {temperature}°C avec {description}."
        else:
            return "Erreur lors de la récupération des informations météo."
