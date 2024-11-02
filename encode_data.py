from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

data = pd.read_pickle("./Data/raw_data.pkl")

channel_encoder = OneHotEncoder(sparse_output=False)
channel_encoded = channel_encoder.fit_transform(data[['channelId']])

category_encoder = OneHotEncoder(sparse_output=False)
category_encoded = category_encoder.fit_transform(data[['categoryId']])

model = SentenceTransformer('all-MiniLM-L6-v2')

title_embeddings = model.encode(data['title'].tolist())
description_embeddings = model.encode(data['description'].tolist())

tag_encoder = MultiLabelBinarizer()
tag_encoded = tag_encoder.fit_transform(data['tags'])

topic_encoder = MultiLabelBinarizer()
topic_encoded = topic_encoder.fit_transform(data['topicCategories'])

encoded_features = np.hstack([
    channel_encoded,
    category_encoded,
    title_embeddings,
    description_embeddings,
    tag_encoded,
    topic_encoded
])

np.save('./Data/encoded_data.npy', encoded_features)

metadata = data[['title', 'channelId', 'channelTitle', 'categoryId', 'thumbnail_url', 'description']]
metadata.to_pickle('./Data/encoded_metadata.pkl')

print("Encoded features saved and metadata extracted.")