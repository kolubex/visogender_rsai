import os
import subprocess
import csv
import pandas as pd

def download_name(url, name, folder):
    # Ensure the folder exists, create if not
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Construct the output file path
    output_path = os.path.join(folder, f"{name}.jpeg")

    # Use subprocess to run the curl command
    try:
        subprocess.run(["curl", "-o", output_path, url], check=True)
        print(f"Image downloaded successfully and saved as {output_path}")
        return 1
    except subprocess.CalledProcessError as e:
        # append the name to the error.log
        with open("error.log", "a") as file:
            file.write(f"{name}, {url}, {folder}\n")
        return 0

def load_tsv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        # make a df from the tsv file
        df = pd.read_csv(file, delimiter='\t')
        # print the first 5 rows of the dataframe
        # print(df.head())
        return df

if __name__ == "__main__":
    # Define the file paths
    file_path_OO = "data/visogender_data/OO/OO_Visogender_02102023.tsv"
    file_path_op02102023 = "data/visogender_data/OP/OP_Visogender_02102023.tsv"
    file_path_op02102023 = "data/visogender_data/OP/OP_Visogender_02102023.tsv"


    # Load the data
    op02102023_df = load_tsv(file_path_op02102023)
    op02102023_df = load_tsv(file_path_op02102023)
    oo_df = load_tsv(file_path_OO)

    # Download the images
    for index, row in op02102023_df.iterrows():
        download_name(row["URL type (Type NA if can't find)"], row['IDX'], "data/visogender_data/OP02102023_images")
        
    for index, row in op02102023_df.iterrows():
        download_name(row["URL type (Type NA if can't find)"], row['IDX'], "data/visogender_data/OP02102023_images")

    for index, row in oo_df.iterrows():
        download_name(row["URL type (Type NA if can't find)"], row['IDX'], "data/visogender_data/OO_images")

    print("All images downloaded successfully")