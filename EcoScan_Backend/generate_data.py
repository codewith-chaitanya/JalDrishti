import pandas as pd
import random
import numpy as np

# 1. Setup: Define some "Known" DNA patterns
species_dna = {
    "Thunnus thynnus (Bluefin Tuna)": "ATCGGCTACGATCGATCGATCGTAGCTAGCTAGCTAGCTG",
    "Gadus morhua (Cod)": "GGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT",
    "Chelonia mydas (Green Turtle)": "TTTTAAAACCCCGGGGATCGATCGTAGCTAGCTAGCTAGC",
}

data = []

# 2. Generate 200 samples
for i in range(200):
    # 90% chance it's a KNOWN species (Normal)
    if random.random() > 0.1:
        species = random.choice(list(species_dna.keys()))
        base_seq = species_dna[species]
        # Add small random mutations (noise)
        seq_list = list(base_seq)
        if random.random() > 0.5:
            seq_list[random.randint(0, len(seq_list)-1)] = random.choice("ATCG")
        final_seq = "".join(seq_list)
        location_name = "Pacific Ocean Zone A"
        lat = 35.0 + random.uniform(-1, 1)
        lon = 139.0 + random.uniform(-1, 1)
    
    # 10% chance it's a NEW ORGANISM (Anomaly)
    else:
        # Completely random DNA sequence
        final_seq = "".join(random.choices("ATCG", k=40))
        location_name = "Uncharted Zone X"
        lat = 0.0 + random.uniform(-2, 2)
        lon = 160.0 + random.uniform(-2, 2)

    data.append({
        "Sequence": final_seq,
        "Location": location_name,
        "Latitude": round(lat, 4),
        "Longitude": round(lon, 4)
    })

# 3. Save to CSV
df = pd.DataFrame(data)
df.to_csv("edna_data.csv", index=False)
print("✅ Success! 'edna_data.csv' has been created.")