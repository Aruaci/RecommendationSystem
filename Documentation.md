# Video Recommendation System Documentation

# Application Description

## Features

This application enables the user to select one of the 100 scraped videos, or by a button click a random one and displays 5 recommendations. The recommendations are ranked by their similarity to the selected video and display the thumbnail, Video Title, Video Author, Description and Similarity Score to the selected video.

## Hosting

The application is hosted on [Streamlit](https://streamlit.io/) and can be accessed here: [https://videorecommendation.streamlit.app/](https://videorecommendation.streamlit.app/)

# Application Code

## 1. Load Data and Extract Features

`load_data.py`

The raw scraped metadata of the videos is saved in JSON files. The first step is to load the raw data and decide which features to use for the recommendation system. Here various statistical feature selection methods could have been performed but due to the scope of the project the features have been selected manually.

The as features selected metadata categories are: `channelId, channelTitle, title, description, tags, categoryId, topicCategories` . For more information on this metadata see [here](https://developers.google.com/youtube/v3/docs/videos#properties).

Additionally `thumbnail_url` is selected for use on the frontend.

## 2. Encode Data

`encode_data.py`

First the `channelId` and `categoryId` are [One-Hot-Encoded](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html). Then a pretrained [BERT Model (all-MiniLM-L6-v2)](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#original-models) is selected. The model is used to encode the concatenated `title` and `description`. The `tags` and `topicCategories` are encoded using a [Multi Label Binarizer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html).

Also the actual values of the selected features are pickled for later display on the frontend.

## 3. Normalise Data

`normalise_data.py`

Using a [Min-Max-Scaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html), the encoded features are normalised.

## 4. Similarity Matrix

`app.py`

The similarity matrix is calculated by taking the [Cosine Similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) of the normalised features. Given a video's index , the similarity matrix and an integer for the number of recommendations, the recommendation function uses similarity matrix to identify the `top_k` most similar videos (excluding the input video) and returns a list of recommendation details, including title, channel name, similarity score, description, and thumbnail URL.

## 5.  Frontend

`app.py`

Using `@st.cache_data` the video metadata (which was saved in Step 2) and normalised final features are loaded.  By caching it, the app only loads this file once per session or until the file changes, reducing the need to repeatedly load the data.

Then Step 4 is done and the recommendations are displayed using Streamlit components such as `st.write`,  `st.expander`, `st.selectbox` or `st.button`.

## Deployment Bugs

Unfortunately in the deployed version a problem repeatedly appears: Sometimes when selecting a video from the dropdown menu, the video is not selected and can only be selected when opening the menu again and selecting the veideo again.

Therefore to test the application it is advised to run it locally.
To run the application the Python packages in requirements.txt need to be installed. 
Once located in the project folder run: `streamlit run app.py`