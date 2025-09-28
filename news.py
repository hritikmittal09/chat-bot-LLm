import requests
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from  utils. spech import speak

url = 'https://newsi-app.com/api/local?language=en&country=us&sort=top&page=1&limit=20'
load_dotenv()
Api_key = os.getenv("news_api_key")


def news():
    my_news = NewsApiClient(api_key=Api_key)
    response = my_news.get_top_headlines()  # 🇮🇳 India
    
    articles = response.get("articles", [])
    
    # ✅ Fetch only descriptions
    descriptions = [article["description"] for article in articles if article.get("description")]
    
    print(descriptions)
    return descriptions  
   
    
    
def fetchNews():
    res = requests.get(url)
    print(res)
if __name__ == "__main__":
    news()    
