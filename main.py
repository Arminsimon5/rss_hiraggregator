from rss_reader import read_rss


rss_url = "https://www.vezess.hu/feed/"

articles = read_rss(rss_url)

for news in articles:
    print("Cím:", news["title"])
    print("Link:", news["link"])
    print("Dátum:", news["published"])
    print("Leírás:", news["summary"])
    print("-" * 50)