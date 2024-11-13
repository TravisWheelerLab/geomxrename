# For Illumina BaseSpace Sequence Hub file format
#
# To convert a file format from
# B04_CKDL230023209-1A_H75KCDSX7_L2_1.fq.gz
# to
# DSP-1001660018726-A-B04_S5_L002_R1_001.fastq.gz
#
# Reads the files and subdirectories of the directory the program is in
#
# Unless it gets the --skip-gzip argument, the script
# re-gzip's the files as the original gzip can be unreadable by the service
# This re-gzipping adds substantial processing time

import os, gzip, argparse, csv

def read_samplesheet(sampleidfile):
    if os.path.exists(sampleidfile):
        try:
            with open(sampleidfile, 'r', encoding='utf-8-sig') as file:
                first_line = file.readline().strip()  # Read the first line and remove leading/trailing whitespace

            if ',' in first_line:
                # If the first line contains commas, treat it as a CSV file
                try:
                    with open(sampleidfile, 'r', encoding='utf-8-sig') as csv_file:
                        try:
                            # Read the CSV file into a list called samplesheet
                            samplesheet = next(csv.reader(csv_file))
                            return samplesheet
                        except csv.Error:
                            print(f"Error: The file '{sampleidfile}' is not a valid CSV file.")
                            return None
                except FileNotFoundError:
                    print(f"Error: The file '{sampleidfile}' exists but couldn't be read.")
                    return None
            else:
                # If the first line does not contain commas, treat it as newline-delimited
                with open(sampleidfile, 'r', encoding='utf-8-sig') as txt_file:
                    # Read the newline-delimited file into a list called samplesheet
                    samplesheet = txt_file.read().splitlines()
                return samplesheet

        except FileNotFoundError:
            print(f"Error: The file '{sampleidfile}' exists but couldn't be read.")
            return None
    else:
        print(f"Error: The file '{sampleidfile}' does not exist.")
        return None

def rename_and_process_files(current_directory, samplename, samplesheet, skip_gzip):
    for root, dirs, files in os.walk(current_directory):
        for file_name in files:
            # Split the filename by a specific delimiter (e.g., "_")
            parts = file_name.split("_")
            if len(parts) == 6:
                del parts[1]

            # Check if there are at least two elements in the split result
            if len(parts) >= 3:
                if parts[0].startswith("S") and parts[0][1:].isdigit():
                    filestart = f'{parts[0]}_{parts[1]}'
                    del parts[0]
                else:
                    filestart = f'{parts[0]}'

                print(filestart)
                try:
                    # Check if filestart matches the second part of any entry in samplesheet
                    matched_index = None
                    for index, entry in enumerate(samplesheet):
                        if entry.endswith(f"_{filestart}"):  # Check if the entry ends with "_<filestart>"
                            matched_index = index
                            break

                    # Construct the "S<element number>" sample sheet location
                    element_number = index + 1
                    S_string = f'S{element_number}'

                    # Remove all this: CKDL230023209-1A_H75KCDSX7
                    del parts[1:3]
                
                    # Store the Lane number
                    fourth_element = parts[1]

                    # Initialize FR with a default value
                    FR = ""
                    if parts[2].startswith("1"):
                        FR = "_R1"
                    elif parts[2].startswith("2"):
                        FR = "_R2"
                    else:
                        print(f"Warning: Unrecognized read type in {file_name}. Expected '1' or '2'.")
                        continue  # Skip to the next file if not recognized
                    
                    parts[1] = S_string + "_" + fourth_element[:1] + "00" + fourth_element[1:] + FR + "_001"
                
                    # Remove the "_1" or "_2"
                    last_element = parts[2]
                    parts[2] = last_element[2:]

                    # Construct the new filename
                    new_file_name = "_".join(parts)
                    new_file_name = new_file_name.replace("_fq", ".fastq")

                    # Construct the old and new file paths
                    old_file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(root, samplename + new_file_name)

                    # Rename the file
                    os.rename(old_file_path, new_file_path)

                    print(f"Processed: {new_file_path}")

                    if not skip_gzip and new_file_path.endswith(".gz"):
                        # Define the output file path for the decompressed content
                        output_file_path = new_file_path.rstrip(".gz")

                        # Open the .gz file and the output file
                        with gzip.open(new_file_path, 'rb', compresslevel=1) as gzipped_file, open(output_file_path, 'wb') as output_file:
                            # Read the compressed content and write it to the output file
                            while True:
                                chunk = gzipped_file.read(1024)
                                if not chunk:
                                    break
                                output_file.write(chunk)

                        # Recompress the decompressed file
                        recompressed_file_path = output_file_path + ".gz"
                        with open(output_file_path, 'rb') as input_file, gzip.open(recompressed_file_path, 'wb') as gzipped_output_file:
                            while True:
                                chunk = input_file.read(1024)
                                if not chunk:
                                    break
                                gzipped_output_file.write(chunk)
                    
                        # Delete the original uncompressed file
                        os.remove(output_file_path)

                except ValueError:
                    print(f"Skipped: {file_name} - Error occurred while processing")  # Handle the error here (or you can leave it blank to just proceed)
            else:
                print(f"Skipped: {file_name} - Unable to split into at least two parts")

def main():
    parser = argparse.ArgumentParser(description="A script that takes two required command-line arguments.")
    
    # Define the first required argument
    parser.add_argument("samplename", help="The SampleName base")

    # Define the second required argument
    parser.add_argument("sampleidfile", help="The CSV file containing sample IDs")

    # Define the --skip-gzip option
    parser.add_argument("--skip-gzip", action="store_true", help="Skip gzip operations")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    samplename = args.samplename
    sampleidfile = args.sampleidfile
    skip_gzip = args.skip_gzip

    samplesheet = read_samplesheet(sampleidfile)

    if samplesheet is not None:
        current_directory = os.getcwd()
        rename_and_process_files(current_directory, samplename, samplesheet, skip_gzip)

if __name__ == "__main__":
    main()