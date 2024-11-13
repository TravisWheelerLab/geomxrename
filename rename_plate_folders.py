import os
import pandas as pd

# Read CSV file
csv_file = 'novogene_key.csv'  # Replace with the path to your CSV file
data = pd.read_csv(csv_file)

# Create a dictionary to store plate and suffix pairs
# Replace null or empty suffix with an empty string
suffix_dict = {str(row['suffix']).strip('_') if pd.notna(row['suffix']) else "": f"S{row['plate']}" for _, row in data.iterrows()}

# Define the directory to look for subdirectories
raw_data_dir = os.path.join(os.getcwd(), '01.RawData')

# Process each subdirectory
for dirname in os.listdir(raw_data_dir):
    dir_path = os.path.join(raw_data_dir, dirname)
    if os.path.isdir(dir_path):
        # Check if dirname is "Undetermined"
        if dirname == "Undetermined":
            # If the dirname is "Undetermined", just pass it along without processing
            new_name = dirname  # Use the original name
        else:
            # Split directory name into root and suffix
            if '_' in dirname:
                root, suffix = dirname.split('_', 1)
                suffix = suffix.strip()
            else:
                root = dirname
                suffix = ""

            # Check if suffix is in suffix_dict to rename
            if suffix in suffix_dict:
                new_name = f"{suffix_dict[suffix]}_{root}"
            else:
                new_name = dirname  # If suffix not found, keep original name

        new_path = os.path.join(raw_data_dir, new_name)

        # Print the rename action
        print(f"Renamed '{dirname}' to '{new_name}'")
        os.rename(dir_path, new_path) 