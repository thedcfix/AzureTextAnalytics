from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

analytics_key = "YOUR_ANALYTICS_KEY"
analytics_endpoint = "YOUR_ANALYTICS_ENDPOINT"

def authenticate_client():
    ta_credential = AzureKeyCredential(analytics_key)

    text_analytics_client = TextAnalyticsClient(
            endpoint=analytics_endpoint, 
            credential=ta_credential, 
            api_version='v3.0')
    
    return text_analytics_client

def fix_text_length(text):
    
    text = str(text)
    final = ''
    
    # maximum text length supported by the analytics service
    max_len = 5120
    
    if (len(text) > max_len):
        chunks = text.split('.')
        
        for chunk in chunks:
            if len(final) + len(chunk) < max_len:
                final = final + "." + chunk
    else:
        final = str(text)
    
    return final

def sentiment_analysis(client, text):

    text = fix_text_length(text)
    
    documents = [text]
    response = client.analyze_sentiment(documents = documents)[0]

    sentiment = response.sentiment
    positive_score = response.confidence_scores.positive
    neutral_score = response.confidence_scores.neutral
    negative_score = response.confidence_scores.negative

    outcome =     {    'sentiment': sentiment,
                    'positive_score': positive_score,
                    'neutral_score': neutral_score,
                    'negative_score': negative_score
                }
    
    return outcome

def key_phrase_extraction(client, text):

    keywords = []
    
    text = fix_text_length(text)
    
    documents = [text]
    response = client.extract_key_phrases(documents = documents)[0]

    if not response.is_error:
        for phrase in response.key_phrases:
            keywords.append(phrase)
    
    return keywords

# creating the text analytics client
analytics_client = authenticate_client()

text = "The dog is under the table. LeBron James dunks on the dog."
text = fix_text_length(text)

outcome = sentiment_analysis(analytics_client, text)
outcome = key_phrase_extraction(analytics_client, text)