import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

@st.cache_data
def load_data():
    data = pd.read_pickle("./Data/encoded_metadata.pkl")
    return data

@st.cache_data
def load_final_features():
    return np.load('./Data/final_features.npy')

data = load_data()
final_features = load_final_features()

similarity_matrix = cosine_similarity(final_features)

def get_recommendations(video_index, similarity_matrix, top_k=5):
    similarity_scores = similarity_matrix[video_index]
    similar_indices = np.argsort(similarity_scores)[::-1]
    similar_indices = similar_indices[similar_indices != video_index]
    top_indices = similar_indices[:top_k]
    top_scores = similarity_scores[top_indices]
    
    recommendations = []
    for idx, score in zip(top_indices, top_scores):
        video_info = {
            "title": data.iloc[idx]["title"],
            "channel": data.iloc[idx]["channelTitle"],
            "similarity_score": score,
            "description" : data.iloc[idx]["description"],
            "thumbnail": data.iloc[idx]["thumbnail_url"]
        }
        recommendations.append(video_info)
    
    return recommendations

if "selected_video_title" not in st.session_state:
    st.session_state["selected_video_title"] = data['title'].tolist()[0]

st.title("Video Recommendation System")

if st.button("Random"):
    st.session_state["selected_video_title"] = random.choice(data['title'].tolist())

selected_video_title = st.selectbox(
    "Select a video:",
    data['title'].tolist(),
    index=data['title'].tolist().index(st.session_state.get("selected_video_title", data['title'].tolist()[0]))
)

st.session_state["selected_video_title"] = selected_video_title
video_index = data[data['title'] == st.session_state["selected_video_title"]].index[0]

recommendations = get_recommendations(video_index, similarity_matrix)

st.header("Recommendations:")
for rec in recommendations:
    st.image(rec['thumbnail'], width=320)
    st.subheader(f"{rec['title']}")
    st.write(f"**Channel:** {rec['channel']}")
    with st.expander("**Descripion**", expanded=False):
        st.write(rec['description'])
    st.write(f"**Similarity Score:** {rec['similarity_score']:.4f}")
    st.write("---")