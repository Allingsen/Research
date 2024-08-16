import tweepy
import pandas as pd


# DEPRECEATED. USE OOP CODE INSTEAD
BEARER_TOKEN= ''
CONSUMER_KEY= ''
CONSUMER_SECRET= ''
ACCESS_TOKEN= ''
ACCESS_TOKEN_SECRET= ''

def main() -> None:
    '''Gets the tweet information of '''
    client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET)

    df = pd.read_csv('./csvs/paper_one.csv')

    ids = set(df['id'].to_list())
    ids = list(ids)

    new_csv = pd.read_csv('oogabooga.csv',index_col='index')

    tweet_fields = ['created_at', 'text']

    # Everytime API requests run out, this should go up by 1500
    start = 6000
    while start < len(ids):
        sub_ids = ids[start:start+100]
        try:
            all_data = client.get_tweets(sub_ids, expansions='author_id', tweet_fields=tweet_fields)

            if all_data.data == None:
                print("No data found. IDs removed.")
            else:
                for i in all_data.data:
                    new_csv.loc[len(new_csv.index)] = [i['id'], i['text'].replace('\n', ' '), i['created_at']]

            print(f'Last ID:{sub_ids[-1]}')
            start+=100

        except:
            break

    new_csv.to_csv('oogabooga.csv')