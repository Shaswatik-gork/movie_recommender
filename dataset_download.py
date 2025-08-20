

import requests
import zipfile
import os

def download_file(url, filename):
    """Downloads a file from a given URL."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")

def extract_zip(zip_filename, extract_path='.'):
    """Extracts a zip file to a specified path."""
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Extracted {zip_filename} to {extract_path}")
    except zipfile.BadZipFile:
        print(f"Error: {zip_filename} is not a valid zip file.")
    except FileNotFoundError:
        print(f"Error: {zip_filename} not found.")

# URL for the larger dataset
ml_1m_url = 'http://files.grouplens.org/datasets/movielens/ml-1m.zip'
zip_filename = 'ml-1m.zip'
extract_path = './ml-1m' # Create a directory to extract the files

# Download and extract the dataset
if not os.path.exists(zip_filename):
    download_file(ml_1m_url, zip_filename)

if os.path.exists(zip_filename):
    extract_zip(zip_filename, extract_path)



