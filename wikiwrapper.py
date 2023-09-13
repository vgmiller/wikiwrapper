import json
from tkinter import W
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def make_request(url, unverified=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'From': 'vanessa.g.miller@gmail.com'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        print("Error with Wikipedia request, Error Code:", response.status_code)
    
    return None

def build_top_views_url_for_date(date):
    base_url = "http://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    return base_url + str(date.year) + f"/{date.month:02d}/" + f"{date.day:02d}"

def build_daily_views_url(article_title, start_date, end_date):
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/"
    return base_url + article_title + f"/daily/{start_date.year:04d}{start_date.month:02d}{start_date.day:02d}00/{end_date.year:04d}{end_date.month:02d}{end_date.day:02d}00"
    
def validate_input_date(date):
    # In case we expose any of this API to outside users, do date format checking
    # If that IS the case, may want to expand the messaging/checking here
    try:
        return datetime.strptime(date, "%Y/%m/%d")
    except ValueError as e:
        print("Date is invalid or " + str(e))
        return None
    
def make_valid_month_date(year, month_number, day):
    return validate_input_date("%s/%s/%s" % (year, month_number, day))

def week(date):
    return date+timedelta(days=6)

def month(date):
    return date+relativedelta(months=+1)-timedelta(days=1)
    
def article_views_for_range(article_title, start_date, end_date):
    count = 0
    url = build_daily_views_url(article_title, start_date, end_date)
    return make_request(url)

def count_views(view_dict):
    count = 0
    if view_dict:
        for day in view_dict['items']:
            count += day['views']
    return count

def article_views_for_week(article_title, start_date):
    date = validate_input_date(start_date)
    if date:
        response = article_views_for_range(article_title, date, week(date))
        if response:
            return count_views(response)
    return None
    
def article_views_for_month(article_title, year, month_number):
    date = make_valid_month_date(year, month_number, 1)
    if date:
        response = article_views_for_range(article_title, date, month(date))
        if response:
            return count_views(response)
    return None

def article_top_view_day_for_month(article_title, year, month_number):
    date = make_valid_month_date(year, month_number, 1)
    if date:
        response = article_views_for_range(article_title, date, month(date))
        if response:
            timestamp = max(response['items'], key=lambda a:a['views'])['timestamp']
            return timestamp[:4]+"/"+timestamp[4:6]+"/"+timestamp[6:8]
    return None

def daterange(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)

def most_viewed_for_range(start_date, end_date):
    results = {}
    for d in daterange(start_date, end_date):
        response = make_request(build_top_views_url_for_date(d))
        if response:
            for page in response['items'][0]['articles']:
                article_name = page['article']
                if results.get(article_name):
                    results[article_name] += page['views'] 
                else:
                    results[article_name] = page['views']        
    return sorted(results, key=results.get, reverse=True) if results else None

def most_viewed_for_week(start_date):
    date = validate_input_date(start_date)
    if date:
        return most_viewed_for_range(date, week(date))
    return None
    
def most_viewed_for_month(year, month_number):
    date = make_valid_month_date(year, month_number, 1)
    if date:
        return most_viewed_for_range(date, month(date))
    return None

def demo():
    print("Hello!")
    print("The top ten most-viewed pages from January 2022 are:")
    res = most_viewed_for_month(2022,1)[:10]
    print(res)
    print("The day that Albert Einstein's page was most viewed in October 2015 is:")
    day = article_top_view_day_for_month("Albert Einstein", 2015, 10)
    print(day)
    print("Goodbye!")

if __name__ == '__main__':
    import sys
    sys.stdout = open(1, 'w', encoding="utf-8", closefd=False) # in case you're running VSCode in Windows like me
    demo()
