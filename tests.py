from wikiwrapper import *

def tests():
    # Test 1 make_request
    response1 = make_request("http://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2015/10/10")
    print("PASS Test 1") if response1 == json.load(open("response1.json", encoding="utf-8")) else print("FAIL Test 1")
    
    # Test 2 build_top_views_url_for_date
    url = build_top_views_url_for_date(datetime(2022,1,10))
    expected_url = "http://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2022/01/10"
    print("PASS Test 2") if url == expected_url else print("FAIL Test 2")
    
    # Test 3 build_daily_views_url
    url = build_daily_views_url("Albert_Einstein", datetime(2015,10,1), datetime(2016,2,20))
    expected_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/2015100100/2016022000"
    print("PASS Test 3") if url == expected_url else print("FAIL Test 3")
    
    # Test 4 article_views_for_range
    response2 = article_views_for_range("Albert_Einstein", datetime(2015,10,1), datetime(2015,10,2))
    print("PASS Test 4") if response2 == json.load(open("response2.json", encoding="utf-8")) else print("FAIL Test 4")
    
    # Test 5 count_views and article_views_for_range
    count = count_views(article_views_for_range("Albert_Einstein", datetime(2015,10,1), datetime(2015,10,2)))
    expected_count = 39676 # count acquired by viewing responses in browser
    print("PASS Test 5") if count == expected_count else print("FAIL Test 5")
    
    # Test 6 article_views_for_week
    count = article_views_for_week("Albert_Einstein", "2015/10/01")
    expected_count = 141161 # count acquired by viewing responses in browser
    print("PASS Test 6") if count == expected_count else print("FAIL Test 6")
    
    # Test 7 articles_views_for_month
    count = article_views_for_week("Albert_Einstein", "2015/10/01")
    # Sorry, not going to manually count these up for verification :)
    print("PASS Test 7") if type(count) == int else print("FAIL Test 7")
    
    # Test 8 article_top_view_day_for_month
    top_day = article_top_view_day_for_month("Albert Einstein", 2015, 10)
    expected_day = "2015/10/29" # acquired by viewing responses in browser
    print("PASS Test 8") if top_day == expected_day else print("FAIL Test 8")
    
    # Test 9 most_viewed_for_range
    top_results = most_viewed_for_range(datetime(2018,3,11), datetime(2018,3,17))
    expected_1 = "Main_Page"
    expected_2 = "Special:Search"
    expected_3 = "Stephen_Hawking" #https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report/March_11_to_17,_2018
    print("PASS Test 9") if top_results[0:3] == [expected_1, expected_2, expected_3] else print("FAIL Test 9")
    
    # Test 10 wikipedia API acknowledges validity but gives 404s
    print("Expect several 404 messages here:")
    result = most_viewed_for_range(datetime(2015,6,7), datetime(2015,6,13))
    #expected_number2 = "Christopher_Lee" #https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report/June_7_to_13,_2015
    expected_result = None
    print("PASS Test 10") if result == expected_result else print("FAIL Test 10")

    # Test 11 non-existent article
    print("Expect one 404 message here:")
    response = article_views_for_week("Alberto_Einstein", "2015/10/01")
    expected_response = None
    print("PASS Test 11") if response == expected_response else print("FAIL Test 11")
    
    # Test 12 validate_date_input and make_valid_month_date
    date1 = make_valid_month_date(2022, 10, 1)
    date2 = make_valid_month_date(2022, 1, 10)
    print("Expect invalid date error message here:")
    date3 = validate_input_date("%s/%s/%s" % (2022, 20, 1))
    validated_dates = [date1, date2, date3]
    expected_dates = [datetime(2022,10,1), datetime(2022,1,10), None]
    print("PASS Test 12") if validated_dates == expected_dates else print("FAIL Test 12")
    
if __name__ == '__main__':
    import sys
    sys.stdout = open(1, 'w', encoding="utf-8", closefd=False) # in case you're running VSCode in Windows like me
    tests()