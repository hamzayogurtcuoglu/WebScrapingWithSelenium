import requests

#Bing API

def bing_news(topic):
    subscription_key = ""
    search_term = topic
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

    headers = {"" : subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    for content in search_results["value"]:
        title = content['name']
        description = content['description']
        url = content['url']
        date = content['datePublished']. split('T')[0], content['datePublished']. split('T')[1].split('.')[0]
        print("-----------------------------")
        print(title)
        print(description)
        print(url)
        print(date)

bing_news("Aselsan") #Haberi istenen başlık buraya yazınız.
