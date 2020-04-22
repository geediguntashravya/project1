import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "slo490C6IvRc6uOMgIzH2A", "isbns": "9781632168146"})
print(res.json())