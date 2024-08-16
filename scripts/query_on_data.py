import pandas as pd
import random


# Query parameters we have decided on (Subject to change)
AI_LIST = ['Artificial Intelligence',
           'Chat-Gpt',
           'GenAI',
           'Generative AI',
           'gemeni',
           'Open-AI',
           'chatgpt4',
           'Chatbot',
           'magicschool',
           'AI',
           'GAI',
           'magic school']

EDU_LIST = ['Education',
            'Academia',
            'Classroom',
            'Teaching',
            'Teach',
            'research',
            'courses',
            'Teaching tools',
            'Online learning',
            'Distance education',
            'Higher education',
            'k-12 education',
            'Teachers',
            'schools',
            'student',
            'educators',
            'professor',
            'personalized learning',
            'test',
            'quiz',
            'assignment',
            'plagiarism',
            'cheating',
            'instructor',
            'college',
            'lesson',
            'edtech',
            'assessment',
            'early childhood education',
            'academic',
            'k-8 education',
            'lesson plans']

# Reads csv
TWEETS = pd.read_csv('./csvs/tweets_categorized.csv')

def get_random_choices(input_list: list) -> list:
    '''Selects a random number of keywords from a given list'''
    chosen = []
    # Random number between 1/2 and full length
    num = random.randint(len(input_list)//2, len(input_list))
    for _ in range(num):
        keyword = random.choice(input_list)
        if keyword not in chosen:
            chosen.append(keyword)
    return chosen

def get_query() -> tuple:
    '''Creates a query using random keywords from both lists'''
    chosen_ai = get_random_choices(AI_LIST)
    chosen_edu = get_random_choices(EDU_LIST)
    return chosen_ai, chosen_edu

def search_tweets(query_ai: list, query_edu: list) -> pd.DataFrame:
    '''Searches the tweets using the query'''
    df = pd.DataFrame(columns=['id','text','Educator','Student','Expert/keynote/researchers'])

    for i in range(len(TWEETS)):
        text = (TWEETS['text'][i]).lower()
        # If the query matches, add it
        if any(ai.lower() in text for ai in query_ai) and any(edu.lower() in text for edu in query_edu):
            df.loc[len(df.index)] = TWEETS.iloc[i]

    return df

def find_percentage(df: pd.DataFrame, query: list) -> tuple:
    '''Finds the percentage of the useful tweets'''
    educator = df[df['Educator'] == 1]
    student = df[df['Student'] == 1]
    expert = df[df['Expert/keynote/researchers'] == 1]

    combined_df = pd.concat([educator, student, expert])
    try:
        percentage = len(combined_df) / len(df)
    except ZeroDivisionError:
        percentage = 0
    info = (percentage, query)

    return info

def main() -> None:
    '''Creates 1000 random queries, returns the top 50'''
    best = []
    for _ in range(1000):
        print(_)
        ai,edu = get_query()
        df = search_tweets(ai, edu)
        combined_query = ai + edu
        tbs = find_percentage(df, combined_query)
        best.append(tbs)
    best.sort(key=lambda x: x[0], reverse=True)
    for i in range(50):
        print('Percentage: ' + str(best[i][0]) + '%', 'Query: ' + str(best[i][1]) + '\n')

if __name__ == '__main__':
    main()