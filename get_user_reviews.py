import requests
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from preprocess_functions import *
def getReviewEndPoint(username):
    url = "https://www.trustpilot.com/search?query={}".format(username)
    response = get(url)
    preferred_url = "{}.com".format(username.lower())
    html_soup = BeautifulSoup(response.text, 'html.parser')
    review_containers = html_soup.find_all('a', class_ = 'search-result-heading')
    for i in range(len(review_containers)):
        if preferred_url in review_containers[i]['href']:
            return review_containers[i]['href']
    try:
        return review_containers[0]['href']
    except:
        return 0
def clean_string(column):
    return column.apply(lambda x: x.replace("\n",'',2)).apply(lambda x: x.replace('  ',''))

def scrape_reviews(PATH, n_pages, sleep_time = 0.3):
    names = []
    ratings = []
    headers = []
    reviews = []
    locations = []
    for p in range(n_pages):
        sleep(sleep_time)
        final_path = "{}{}".format(PATH,p)
        try:
            http = requests.get(final_path)
            bsoup = BeautifulSoup(http.text, 'html.parser')

            review_containers = bsoup.find_all('div', class_ = 'review-content__body')
            user_containers = bsoup.find_all('div', class_ = 'consumer-information__name')
            rating_container = bsoup.find_all('div',class_ = "star-rating star-rating--medium")
            location_container = bsoup.find_all('div',class_ = "consumer-information__location")


            for x in range(len(review_containers)):

                review_c = review_containers[x]
                try:
                    reviews.append(review_c.p.text)
                    headers.append(review_c.h2.a.text)
                except:
                    reviews.append("No review")
                    headers.append("No review")
                try:
                    reviewer = user_containers[x]
                    names.append(reviewer.text)
                except:
                    names.append("Name not found")
                try:
                    rating = rating_container[x].img['alt']
                    ratings.append(rating)
                except:
                    ratings.append("Ratings not found")
                try:
                    location = location_container[x]
                    user_loc = location.span.text
                    locations.append(user_loc)
                except:
                    locations.append("Not Found")

            rev_df = pd.DataFrame(list(zip(headers, reviews, ratings, names,locations )),
                          columns = ['Header','Review','Rating', 'Name','Location'])
            rev_df.Header = clean_string(rev_df.Header)
            rev_df.Review = clean_string(rev_df.Review)
            rev_df.Name = clean_string(rev_df.Name)
            rev_df.Location = clean_string(rev_df.Location)
            scrape_success = 1
        except:
            scrape_success = 0
            rev_df = "Error"
            return (rev_df, scrape_success)
    return (rev_df,scrape_success)

    
