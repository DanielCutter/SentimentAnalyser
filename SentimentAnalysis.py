from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import matplotlib.pyplot as plt
import config

# APIs, tweepy, matplotlib, sentiment analysis

analyser = SentimentIntensityAnalyzer()

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)
api = tweepy.API(auth)
# api.wait_on_rate_limit = True

def percentage(part, whole):
    return 100 * float(part)/float(whole)

search_term = input("Enter a search term: ")
number_of_tweets = int(input("How many tweets would you like to analyse?: "))

tweets = tweepy.Cursor(api.search, q=search_term, lang="en", tweet_mode="extended").items(number_of_tweets) 

positive = 0
negative = 0
neutral = 0
i = 0

for tweet in tweets:

    try:
        analyse = analyser.polarity_scores(tweet.retweeted_status.full_text)
    except AttributeError:  # Not a Retweet
        analyse = analyser.polarity_scores(tweet.full_text)

    i += 1

    analysis = analyse["compound"]
    
    if (analysis > 0.05):
        positive += 1
    elif (analysis <= 0.05 and analysis >= -0.05):
        neutral += 1
    elif (analysis < -0.05):
        negative += 1

positive = percentage(positive, i)
negative = percentage(negative, i)
neutral = percentage(neutral, i)

positive = format(positive, ".2f")
negative = format(negative, ".2f")
neutral = format(neutral, ".2f")

labels = ["Positive [" + str(positive) + "%]", "Neutral [" + str(neutral) + "%]", "Negative [" + str(negative) + "%]"]
sizes = [positive, neutral, negative]
colours = ["yellowgreen", "gold", "red"]
patches, texts = plt.pie(sizes, colors = colours, explode=(0.1, 0.1, 0.1), startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting about " + str(search_term) + " (Via an analysis of " + str(i) +" tweets).")
plt.axis("equal")
plt.tight_layout
plt.show()