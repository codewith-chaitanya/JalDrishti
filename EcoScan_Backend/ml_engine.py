import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

def analyze_edna(df: pd.DataFrame):
    # --- STEP 1: PREPARE THE DATA ---
    # We use "K-mers" (substrings of length 3) to turn DNA strings into numbers.
    # Example: "ATCG" becomes counts of [ATC, TCG, ...]
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3))
    
    # Convert the 'Sequence' column into a matrix of numbers
    X = vectorizer.fit_transform(df['Sequence']).toarray()

    # --- STEP 2: DETECT ANOMALIES ---
    # Isolation Forest isolates observations by randomly selecting a feature.
    # Anomalies are easier to isolate (shorter path), so they get a score of -1.
    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly_score'] = model.fit_predict(X)

    # Label them: -1 is "New Organism", 1 is "Known Species"
    df['status'] = df['anomaly_score'].apply(lambda x: 'New Organism' if x == -1 else 'Known Species')

    # --- STEP 3: SIMPLIFY FOR VISUALIZATION (PCA) ---
    # Reduce the complex matrix X into just 2 numbers (x, y) so we can plot it.
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X)
    
    df['pca_x'] = coords[:, 0]
    df['pca_y'] = coords[:, 1]

    # Clean up: remove the raw score column before sending to frontend
    del df['anomaly_score']

    # Convert to a dictionary (JSON format)
    return df.to_dict(orient='records')