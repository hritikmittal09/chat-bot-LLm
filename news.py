import requests
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from spech import speak

url = 'https://newsi-app.com/api/local?language=en&country=us&sort=top&page=1&limit=20'
load_dotenv()
Api_key = os.getenv("news_api_key")


def news():
   # load_dotenv()
    my_news = NewsApiClient(api_key=Api_key)
    response = my_news.get_top_headlines()  # 🇮🇳 India
    
   # print("DEBUG Response:", response)  # 👈 check what API returns
    
    articles = response.get("articles", [])
    titles = [article["title"] for article in articles if article.get("title")]

    return titles  
   
    
    
def fetchNews():
    res = requests.get(url)
    print(res)
if __name__ == "__main__":
    news()    
