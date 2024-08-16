import tweepy
import spacy
import string
import pandas as pd
from collections import Counter
from playwright.sync_api import sync_playwright

class Scraper():
    def __init__(self, df: pd.DataFrame) -> None:
        # Tweepy/X api tokens/keys
        BEARER_TOKEN= ''
        CONSUMER_KEY= ''
        CONSUMER_SECRET= ''
        ACCESS_TOKEN= ''
        ACCESS_TOKEN_SECRET= ''
        self.client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET)
        
        # Query that we have decided (These will be modified)
        self.query = '("artificial intelligence" OR "Chat GPT" OR genAI OR "generative AI" OR gemeni OR Open-AI OR chatgpt4 OR chatbot OR "magic school") ("elementary education" OR "AI literacy" OR education OR academia OR classroom OR teaching OR teach OR courses OR "teaching tools" OR "online learning" OR "distance education" OR "higher education" OR "k-12 education" OR teachers OR schools OR student OR educators OR professor OR "personalized learning" OR test OR quiz OR assignment) -is:retweet lang:en'
        
        # Expansions to get more data from tweets
        self.expans = ['author_id',
                       'referenced_tweets.id']
        self.tweet_fields = ['created_at',
                             'text']
        
        # Number of tweets pulled
        self.TWEET_NUMBER = 10
        
        self.df = df
        self.off_topic = []

    def get_tweet_data(self, until:str=None) -> str:
        '''Collects data using the query provided, uses oldest ID'''
        info = self.client.search_recent_tweets(self.query, max_results=self.TWEET_NUMBER, until_id=until, expansions=self.expans, tweet_fields=self.tweet_fields)
        return info

    def get_ids(self,data:str) -> str:
        '''Places tweets collected into a dataframe, returns the oldest ID'''
        for i in data.data:
            self.df.loc[len(self.df.index)] = [i['id'], i['text'].replace('\n', ' '), i['created_at']] 
        return data.meta['oldest_id']
    
    def get_df_in_csv(self) -> pd.DataFrame:
        '''Converts pandas DF to csv'''
        self.df.to_csv('tweets_new_2.csv')

    def get_all_common_words(self) -> list:
        '''Gets the 100 most common words from tweets, disregarding off-topic and stop words'''
        words_freq = []
        text = self.df['text'].astype(str)
        # Loads in spacy stop words
        nlp = spacy.load("en_core_web_sm")
        for i in text:
            doc = nlp(i)
            # Checks that the words are actually relevant
            filtered_words = [token.text for token in doc if not token.is_stop 
                              and len(token.text) > 1 
                              and token.text not in string.whitespace 
                              and token.text not in string.punctuation
                              and token.text not in self.query 
                              and token.text not in self.off_topic]
            words_freq += filtered_words

        counter = Counter(words_freq)
        most_occur = counter.most_common(100) 
    
        print(most_occur)
        return [key for key, _ in most_occur]
    
    def scrape_tweet_unofficial(self, url: str, context) -> dict:
        '''Scrapes tweets from a given ID. Does NOT use official API'''
        _xhr_calls = []

        def intercept_response(response):
            """capture all background requests and save them"""
            # we can extract details from background requests
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        page = context.new_page()
        # enable background request intercepting:
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        page.goto(url)
        try:
            page.wait_for_selector("[data-testid='tweet']", timeout=10000)
        except:
            page.close()
            return
        # find all tweet background requests:     
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            tweet_data = data['data']['tweetResult']['result']['legacy']
            # Try/except for retweets. This will allow for both to be taken
            try:
                text = tweet_data['retweeted_status_result']['result']['legacy']['full_text']
            except:
                text = tweet_data['full_text']

        page.close()
        return text
    
    def scrape_tweet_offical(self) -> None:
        '''Gets the tweet information of '''

        df = pd.read_csv('./csvs/paper_one.csv')

        ids = set(df['id'].to_list())
        ids = list(ids)

        new_csv = pd.read_csv('oogabooga.csv',index_col='index')

        # Everytime API requests run out, this should go up by 1500
        start = 6000
        while start < len(ids):
            # The api can only search up to 100 tweets at a time
            sub_ids = ids[start:start+100]
            try:
                all_data = self.client.get_tweets(sub_ids, expansions='author_id', tweet_fields=self.tweet_fields)

                # If no tweets are found, remove the IDS
                if all_data.data == None:
                    print("No data found. IDs removed.")
                else:
                    # Add the data to DF
                    for i in all_data.data:
                        new_csv.loc[len(new_csv.index)] = [i['id'], i['text'].replace('\n', ' '), i['created_at']]

                # Useful for multiple queries
                print(f'Last ID:{sub_ids[-1]}')
                start+=100

            except:
                break

        new_csv.to_csv('oogabooga.csv')

# MAIN SCRIPTS
def api_main() -> None:
    '''Gets tweets using the query from the official API'''
    df = pd.DataFrame(columns=['id', 'text', 'created_at'])
    oldest = None
    scraper = Scraper(df)
    num_of_times = 10
    for _ in range(num_of_times):
        # Collects the tweets, inserts them into a DF
        all_data = scraper.get_tweet_data(oldest)
        oldest = scraper.get_ids(all_data)  
        print(oldest)  

    # DF -> CSV
    scraper.get_df_in_csv()
    
def scrape_main_unofficial() -> None:
    '''Gets tweets using webscraping methods'''

    # Reads in csv
    df = pd.read_csv('./csvs/tweets_from_paper_2.csv', index_col='index')
    scraper = Scraper(df)
    file = open('./csvs/read/paper_one.csv', 'r')
    
    # Gets all IDs
    ids = file.readlines()

    start = 6000    # What index to start scraping at
    sub_ids = ids[start:]
    with sync_playwright() as pw:
        # Opens a new window
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        try:
            for i in sub_ids:
                # Scrapes the tweet at the given ID
                num = i.strip()
                url = "https://twitter.com/anyuser/status/" + num
                x = scraper.scrape_tweet_unofficial(url, context)
                # If there is data, add it to the DF
                if x != None:
                    df.loc[len(df.index)] = [num, x.replace('\n', ' ')]
                    print(i)
        finally:
            df.to_csv('./csvs/tweets_from_paper_2.csv')

#def common_words_main() -> None:


if __name__ == '__main__':
    #api_main()
    scrape_main_unofficial()