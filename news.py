import requests
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

url = 'https://newsi-app.com/api/local?language=en&country=us&sort=top&page=1&limit=20'
load_dotenv()
Api_key = os.getenv("news_api_key")


def news():
    my_news = NewsApiClient(api_key=Api_key)
    response = my_news.get_top_headlines(country='in')  # India
    
    articles = response.get("articles", [])
    
    # ✅ Fetch only descriptions
    descriptions = [article["description"] for article in articles if article.get("description")]
    
    return descriptions  
   
    
    
def fetchNews():
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        articles = data.get("articles", [])
        descriptions = [article.get("description", "") for article in articles if article.get("description")]
        return descriptions
    else:
        print(f"Error: {res.status_code}")
        return []
if __name__ == "__main__":
    news()    
