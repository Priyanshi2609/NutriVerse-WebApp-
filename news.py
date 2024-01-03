import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os
# Get today's date
today = datetime.now()

# Calculate the date of two days ago
two_days_ago = today - timedelta(days=2)
# Format the date in 'YYYY-MM-DD' format
two_days_ago_formatted = two_days_ago.strftime('%Y-%m-%d')
news_api_key=os.getenv('NEWS_API_KEY')
news_query="nutrition+facts"


def get_all_posts():
    news_response=requests.get(f"https://newsapi.org/v2/everything?q={news_query}&from={two_days_ago_formatted}&sortBy=publishedAt&apiKey={news_api_key}")
    news_data=news_response.json().get("articles")
    posts=[]
    number=1
    for i in news_data:
        posted_date=i["publishedAt"]
    
        dict={"id":number,"author":i["author"],"title":i["title"],"posted_on":posted_date[:10],"url":i["url"]}
        posts.append(dict)
        number+=1
    return posts
