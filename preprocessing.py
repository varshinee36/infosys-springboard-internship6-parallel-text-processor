# import os
# import re
# import pandas as pd
# import nltk
# from nltk.corpus import stopwords



# def clean_text(text):
#     text = str(text)
#     text = re.sub(r'http\S+|www\S+', '', text)
#     text = re.sub(r'@\w+', '', text)
#     text = re.sub(r'#', '', text)
#     text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
#     text = text.lower()
#     text = text.strip()
#     return text


# def preprocess_tweets(tweet_folder_path):
   

    
#     all_tweets = []

    
#     stop_words = set(stopwords.words('english'))

    
#     event_folders = os.listdir(tweet_folder_path)
#     print(f"  Found {len(event_folders)} event folders")

    
#     for folder in event_folders:

        
#         folder_path = os.path.join(tweet_folder_path, folder)

       
#         if not os.path.isdir(folder_path):
#             continue

        
#         csv_path = os.path.join(folder_path, f'{folder}-tweets_labeled.csv')

        
#         if not os.path.exists(csv_path):
#             continue

        
#         df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')

        
#         if ' Informativeness' in df.columns:
#             df = df[df[' Informativeness'] != 'Not related']

        
#         if ' Tweet Text' not in df.columns:
#             continue

        
#         for tweet in df[' Tweet Text']:

            
#             cleaned = clean_text(tweet)

            
#             words = cleaned.split()

           
#             words = [w for w in words if w not in stop_words]

            
#             if len(words) >= 3:
#                 all_tweets.append(cleaned)

#     print(f"  Total clean tweets collected: {len(all_tweets)}")
#     return all_tweets



# def preprocess_whatsapp(whatsapp_file_path):
#     """
#     Reads and cleans the WhatsApp chat CSV file.
#     Input:  path to Whatsapp_chat.csv
#     Output: list of cleaned messages, dictionary of sender message counts
#     """

#     all_messages = []
#     sender_counts = {}
#     stop_words = set(stopwords.words('english'))

    
#     df = pd.read_csv(whatsapp_file_path, encoding='utf-8', on_bad_lines='skip')

#     print(f"  Total rows in file: {len(df)}")

    
#     for _, row in df.iterrows():

        
#         message = str(row['message'])
#         sender  = str(row['names'])

        
#         cleaned = clean_text(message)

        
#         words = cleaned.split()
#         words = [w for w in words if w not in stop_words]

        
#         if len(words) >= 2:
#             all_messages.append(cleaned)

            
#             if sender not in sender_counts:
#                 sender_counts[sender] = 0
#             sender_counts[sender] += 1

#     print(f"  Total clean messages collected: {len(all_messages)}")
#     print(f"  Total unique senders: {len(sender_counts)}")
#     return all_messages, sender_counts



# if __name__ == "__main__":
#     print("=" * 45)
#     print("Testing preprocess_tweets()")
#     print("=" * 45)
#     tweets = preprocess_tweets("data/tweets")
#     print("\nFirst 3 cleaned tweets:")
#     for i, tweet in enumerate(tweets[:3]):
#         print(f"  {i+1}. {tweet}")

#     print()
#     print("=" * 45)
#     print("Testing preprocess_whatsapp()")
#     print("=" * 45)
#     messages, senders = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
#     print("\nFirst 3 cleaned messages:")
#     for i, msg in enumerate(messages[:3]):
#         print(f"  {i+1}. {msg}")
#     print("\nTop 3 most active senders:")
#     sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)
#     for sender, count in sorted_senders[:3]:
#         print(f"  {sender}: {count} messages")


import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords

try:
    STOP_WORDS = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))


def clean_text(text):
    text = str(text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    return text


# ─────────────────────────────────────────────────────────────
# REAL-TIME CLEANING  ← THIS WAS MISSING IN YOUR VERSION
# ─────────────────────────────────────────────────────────────
def clean_text_realtime(text: str) -> str:
    """Clean text and strip stopwords — used by the dashboard real-time tab."""
    cleaned = clean_text(text)
    words = [w for w in cleaned.split() if w not in STOP_WORDS]
    return " ".join(words)


def preprocess_tweets(tweet_folder_path):
    all_tweets = []
    stop_words = set(stopwords.words('english'))

    event_folders = os.listdir(tweet_folder_path)
    print(f"  Found {len(event_folders)} event folders")

    for folder in event_folders:
        folder_path = os.path.join(tweet_folder_path, folder)
        if not os.path.isdir(folder_path):
            continue

        csv_path = os.path.join(folder_path, f'{folder}-tweets_labeled.csv')
        if not os.path.exists(csv_path):
            continue

        df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')

        if ' Informativeness' in df.columns:
            df = df[df[' Informativeness'] != 'Not related']

        if ' Tweet Text' not in df.columns:
            continue

        for tweet in df[' Tweet Text']:
            cleaned = clean_text(tweet)
            words = [w for w in cleaned.split() if w not in stop_words]
            if len(words) >= 3:
                all_tweets.append(cleaned)

    print(f"  Total clean tweets collected: {len(all_tweets)}")
    return all_tweets


def preprocess_whatsapp(whatsapp_file_path):
    all_messages = []
    sender_counts = {}
    stop_words = set(stopwords.words('english'))

    df = pd.read_csv(whatsapp_file_path, encoding='utf-8', on_bad_lines='skip')
    print(f"  Total rows in file: {len(df)}")

    for _, row in df.iterrows():
        message = str(row['message'])
        sender  = str(row['names'])

        cleaned = clean_text(message)
        words = [w for w in cleaned.split() if w not in stop_words]

        if len(words) >= 2:
            all_messages.append(cleaned)
            sender_counts[sender] = sender_counts.get(sender, 0) + 1

    print(f"  Total clean messages collected: {len(all_messages)}")
    print(f"  Total unique senders: {len(sender_counts)}")
    return all_messages, sender_counts


if __name__ == "__main__":
    print("=" * 45)
    print("Testing preprocess_tweets()")
    print("=" * 45)
    tweets = preprocess_tweets("data/tweets")
    print("\nFirst 3 cleaned tweets:")
    for i, tweet in enumerate(tweets[:3]):
        print(f"  {i+1}. {tweet}")

    print()
    print("=" * 45)
    print("Testing preprocess_whatsapp()")
    print("=" * 45)
    messages, senders = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
    print("\nFirst 3 cleaned messages:")
    for i, msg in enumerate(messages[:3]):
        print(f"  {i+1}. {msg}")
    print("\nTop 3 most active senders:")
    sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)
    for sender, count in sorted_senders[:3]:
        print(f"  {sender}: {count} messages")
