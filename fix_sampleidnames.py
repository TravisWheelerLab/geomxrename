import os
import pandas as pd

# Paths to input files
csv_file = 'novogene_key.csv'  # Replace with the path to your CSV file

# Find the directory starting with "02.Report_" in the current working directory
base_dir = os.getcwd()
report_dir = next((d for d in os.listdir(base_dir) if d.startswith("02.Report_") and os.path.isdir(os.path.join(base_dir, d))), None)

# Verify if the report directory exists
if report_dir is None:
    raise FileNotFoundError("No directory starting with '02.Report_' found in the current directory.")

# Construct the path to the tab-delimited file within the found report directory
xls_file = os.path.join(base_dir, report_dir, 'src', 'tables', 'qc.summary.xls')

# Load the CSV file and create a dictionary for suffix to plate mapping
data = pd.read_csv(csv_file)
suffix_dict = {str(row['suffix']).strip('_') if pd.notna(row['suffix']) else "": f"S{row['plate']}" for _, row in data.iterrows()}

# Load the tab-delimited file and read only column A
xls_data = pd.read_csv(xls_file, sep='\t', usecols=[0], header=0, names=['sample'])  # header=0 removes header
processed_samples = []

# Process each sample in column A according to the renaming rules
for sample in xls_data['sample']:
    # If the sample is "Undetermined", pass it through without processing
    if sample == "Undetermined":
        processed_samples.append(sample)
        continue  # Skip further processing for this sample

    # Check if sample has a suffix
    if '_' in sample:
        root, suffix = sample.split('_', 1)
        suffix = suffix.strip()
    else:
        root = sample
        suffix = ""
    
    # Apply renaming logic based on suffix
    if suffix in suffix_dict:
        new_name = f"{suffix_dict[suffix]}_{root}"
    else:
        new_name = sample  # Keep original if no suffix match

    processed_samples.append(new_name)

# Save the result as a single-column CSV file
output_file = os.path.join(base_dir, 'sampleidnames.csv')
pd.DataFrame(processed_samples, columns=['sample']).to_csv(output_file, index=False, header=False)
print(f"Processed samples saved to '{output_file}'")