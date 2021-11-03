############################################################################################################################
#   AZURE TEXT ANALYSIS AI DEMO - Antony Millington (c)2021 Resonate
#   textanalytics.py
#   This analyses an series of text files containing verbose text (customer feedback used in example)
#   and extracts the key phrases in the text, measures sentiment, and extracts useful entities.
# 
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

cog_key = 'f0144c1b690847a4829bbd3abafb6f2e'
cog_endpoint = 'https://cog-multi-csdev.cognitiveservices.azure.com/'

# 
# STEP 1: Read and display all the reviews which have been left...
#
reviews_folder = os.path.join('text', 'reviews')
# Create a collection of reviews with id (file name) and text (contents) properties
reviews = []
for file_name in os.listdir(reviews_folder):
    review_text = open(os.path.join(reviews_folder, file_name)).read()
    review = {"id": file_name, "text": review_text}
    reviews.append(review)


# 
# STEP 2: Initiate the Text Analytics service...
#

# Get a client for your text analytics cognitive service resource
text_analytics_client = TextAnalyticsClient(endpoint=cog_endpoint,credentials=CognitiveServicesCredentials(cog_key))
# Analyze the reviews you read from the /data/reviews folder earlier
language_analysis = text_analytics_client.detect_language(documents=reviews)

# 
# STEP 3: Extract Key Phrases...
#

# # Use the client and reviews you created in the previous code cell to get key phrases
key_phrase_analysis = text_analytics_client.key_phrases(documents=reviews)
# print key phrases for each review
for review_num in range(len(reviews)):
    # print the review id
    print(reviews[review_num]['id'])
    # Get the key phrases in this review
    print('\nKey Phrases:')
    key_phrases = key_phrase_analysis.documents[review_num].key_phrases
    # Print each key phrase
    for key_phrase in key_phrases:
        print('\t', key_phrase)
    print('\n')

# 
# STEP 4: Perform some sentiment analysis...
#

# Use the client and reviews you created previously to get sentiment scores
sentiment_analysis = text_analytics_client.sentiment(documents=reviews)
# Print the results for each review
for review_num in range(len(reviews)):
    # Get the sentiment score for this review
    sentiment_score = sentiment_analysis.documents[review_num].score

    # classifiy 'positive' if more than 0.5, 
    if sentiment_score < 0.5:
        sentiment = 'negative'
    else:
        sentiment = 'positive'

    # print file name and sentiment
    print('{} : {} ({})'.format(reviews[review_num]['id'], sentiment, sentiment_score))

# 
# STEP 5: Extract Useful Entities...
#

# Use the client and reviews you created previously to get named entities
entity_analysis = text_analytics_client.entities(documents=reviews)
# Print the results for each review
for review_num in range(len(reviews)):
    print(reviews[review_num]['id'])
    # Get the named entitites in this review
    entities = entity_analysis.documents[review_num].entities
    for entity in entities:
        # Only print datetime or location entitites
        if entity.type in ['DateTime','Organization']:
            link = '(' + entity.wikipedia_url + ')' if entity.wikipedia_id is not None else ''
            print(' - {}: {} {}'.format(entity.type, entity.name, link))


