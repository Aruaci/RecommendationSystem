# Normalization script
from sklearn.preprocessing import MinMaxScaler
import numpy as np

encoded_features = np.load('./Data/encoded_data.npy') 

scaler = MinMaxScaler()

normalized_features = scaler.fit_transform(encoded_features)

np.save('./Data/final_features.npy', normalized_features)
print("Normalized features saved to ./Data/final_features.npy")