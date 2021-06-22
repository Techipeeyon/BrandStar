# BrandStar
BrandStar is a web application built using Flask which provides an analytical solution for the companies who want to analyze their product.


## Inspiration 
There are not tools online that provide a way to analyze your own product. A person could hire an analyst for the same but what if this could be done free-of-cost. This really is the inspiration behind building BrandStar

## Features Provided

![features provided](https://user-images.githubusercontent.com/53506835/122927548-9c856b80-d386-11eb-8168-0d764878f4d2.png)


## How we built it
Firstly BrandStar gets the tweets based on the handle provided and gathers this data and cleans it. Using the API provided from expert.ai, it gets the sentiments, behavior, etc from this data and it is then visualized using Plotly. For the user reviews, we try to scrape reviews from Trustpilot based on the username provided and show various visualizations related to ratings, user locations, emotions of users, and much more.

## Setup the Project:
1. Clone the repo.
```
git clone https://github.com/lazyCodes7/BrandStar.git
```
2. Go to the directory.
```
cd BrandStar
```
3. Activate the virtual environment
```
. vemv/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. How to get credentials?
For credentials make an account on expert.ai and also a twitter dev account and get the tokens to be used in the steps below.


6. Create a .env file with these credentials
```
ACCESS_KEY = ""
ACCESS_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
EMAIL= ""
PASSWORD=""
```


7. Run app
```
python app.py
```
8. Open the link in Google Chrome(other browsers might not work, hence Google Chrome)
```
127.0.0.1:5000
```

## Challenges we ran into
Though there were a lot of challenges, I was still able to get through them.
- Getting the tweets and gathering the data
- Understanding how to use expert.ai API
- Using it in my application properly
- Scraping user reviews was a bit challenging as I didn't know where to scrape from

## Accomplishments that we're proud of
- I don't really do web applications so I had to learn Flask a bit before I could build this but I am really satisfied with the end result.
- Building an app that will be useful and could possibly help companies in analyzing brands!

## What we learned
- Learned how to use Flask
- Learned how to use expert.ai API


## What's next for BrandStar
- Enabling users to compare two brands at a time
- Reducing response time for the various routes



