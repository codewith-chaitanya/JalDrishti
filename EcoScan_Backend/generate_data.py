import pandas as pd
import random
import uuid
import os

# 1. ENHANCED SETUP: Define Species with Metadata
species_library = {
    "Thunnus thynnus": {"common_name": "Bluefin Tuna", "seq": "ATCGGCTACGATCGATCGATCGTAGCTAGCTAGCTAGCTG"},
    "Gadus morhua": {"common_name": "Atlantic Cod", "seq": "GGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT"},
    "Chelonia mydas": {"common_name": "Green Turtle", "seq": "TTTTAAAACCCCGGGGATCGATCGTAGCTAGCTAGCTAGC"},
}

def generate_edna_dataset(filename="edna_data.csv", num_samples=200):
    data = []
    
    for _ in range(num_samples):
        sample_id = str(uuid.uuid4())[:8] # Unique ID for every sample
        
        # 90% Probability: Known Species
        if random.random() > 0.1:
            species_id = random.choice(list(species_library.keys()))
            base_info = species_library[species_id]
            
            # BUG FIX: Better Mutation Logic (Simulating Sequencing Noise)
            seq_list = list(base_info["seq"])
            mutation_rate = 0.05 # 5% chance per base
            for j in range(len(seq_list)):
                if random.random() < mutation_rate:
                    seq_list[j] = random.choice("ATCG")
            
            final_seq = "".join(seq_list)
            label = species_id
            location = "Marine Protected Area Alpha"
            lat = 35.0 + random.uniform(-1, 1)
            lon = 139.0 + random.uniform(-1, 1)
        
        # 10% Probability: Anomaly (New/Invasive Species)
        else:
            # BUG FIX: Ensure anomaly length varies slightly
            length = random.randint(35, 45)
            final_seq = "".join(random.choices("ATCG", k=length))
            label = "Unknown_Taxon"
            location = "Deep Sea Trench X"
            lat = round(random.uniform(-90, 90), 4) # Global range
            lon = round(random.uniform(-180, 180), 4)

        data.append({
            "Sample_ID": sample_id,
            "Sequence": final_seq,
            "Species_Label": label,
            "Location": location,
            "Latitude": round(lat, 4),
            "Longitude": round(lon, 4),
            "Environmental_Temp_C": round(random.uniform(4.0, 28.0), 1) # Added Feature for ML
        })

    # 3. SAVE WITH ERROR CHECKING
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Success! {filename} created with {num_samples} samples.")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")

if __name__ == "__main__":
    generate_edna_dataset()