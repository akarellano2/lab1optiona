import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='5Jnr0s0iAEZmZQ',
                     client_secret='MKgZX_ghqG65asMuqq9K354mvhA',
                     user_agent='my user agent'
                     )

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


# recursive method which divides comments into different lists
def process_comments(comments_list, neu_list, p_list, n_list):
    # for each loop to go through every single comment one by one until there is no more comments
    for comments in comments_list:

        # if and else if statements that use the probabilities methods result to .5 to see in
        # which list the comment better fits in
        if get_text_neutral_proba(comments.body) >= 0.5:
            neu_list.append(comments.body)

        elif get_text_positive_proba(comments.body) >= 0.5:
            p_list.append(comments.body)

        elif get_text_negative_proba(comments.body) >= 0.5:
            n_list.append(comments.body)

        # recursive call with replies of top comment
        process_comments(comments.replies, neu_list, p_list, n_list)


def main():
    comments = get_submission_comments(
        'https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    # lists of were the comments will be divided to
    neu_list = list()
    p_list = list()
    n_list = list()

    # calling the recursive made with the comments list already made and the 3 new lists made
    process_comments(comments, neu_list, p_list, n_list)

    # printing out all of the comments that are already in corresponding list
    print("Neutral Comments:")
    print(*neu_list, sep='\n')

    print("")

    print("Positive Comments:")
    print(*p_list, sep='\n')

    print("")

    print("Negative Comments:")
    print(*n_list, sep='\n')

main()
