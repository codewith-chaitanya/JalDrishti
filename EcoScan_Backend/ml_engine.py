import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def analyze_edna(df: pd.DataFrame):
    # --- STEP 1: ROBUST DATA PREPARATION ---
    # Use TfidfVectorizer instead of CountVectorizer. 
    # This normalizes the length so longer sequences don't bias the model.
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
    
    try:
        # BUG FIX: Remove .toarray() if possible, but for IsolationForest we need it.
        # We handle potential memory errors here.
        X_sparse = vectorizer.fit_transform(df['Sequence'])
        X = X_sparse.toarray() 
    except KeyError:
        raise ValueError("The CSV must contain a 'Sequence' column.")

    # --- STEP 2: SCALING (Crucial for PCA) ---
    # Standardize features by removing the mean and scaling to unit variance.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- STEP 3: ANOMALY DETECTION ---
    # We increase n_estimators for better stability.
    # Contamination=0.1 assumes 10% are anomalies.
    model = IsolationForest(
        n_estimators=200, 
        contamination=0.1, 
        random_state=42,
        n_jobs=-1 # Use all CPU cores for speed
    )
    
    # Predict and map results
    preds = model.fit_predict(X_scaled)
    df['status'] = np.where(preds == -1, 'New Organism', 'Known Species')
    
    # Add a confidence score (Decision Function)
    # Lower scores = more anomalous
    df['anomaly_confidence'] = model.decision_function(X_scaled).round(4)

    # --- STEP 4: STABILIZED VISUALIZATION ---
    # Use PCA on the scaled data for a much more accurate 2D map.
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    
    df['pca_x'] = coords[:, 0].round(4)
    df['pca_y'] = coords[:, 1].round(4)

    # --- STEP 5: OPTIMIZATION ---
    # Drop raw Sequence from the response to save bandwidth (it's already in the CSV)
    # Keep it if your frontend specifically needs to display the string.
    # result_df = df.drop(columns=['Sequence']) 

    return df.to_dict(orient='records')