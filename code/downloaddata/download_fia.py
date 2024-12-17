import os
import pandas as pd
import requests
from tqdm import tqdm
from config import RAW_DIR

import warnings
warnings.filterwarnings('ignore')

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

class DownloadFIA():
    def downloadFile(url, file, download_path):
        r = requests.get(url.format(file), 
                        allow_redirects=True)
        
        open(download_path.format(file), 'wb').write(r.content)

    def download_fia():

        states = { "Alabama": "AL", "Kentucky": "KY", "Ohio": "OH", 
                "Alaska": "AK", "Louisiana": "LA", "Oklahoma": "OK", 
                "Arizona": "AZ", "Maine": "ME", "Oregon": "OR", 
                "Arkansas": "AR", "Maryland": "MD", "Pennsylvania": "PA", 
                "American Samoa": "AS", "Massachusetts": "MA", "Puerto Rico": "PR", 
                "California": "CA", "Michigan": "MI", "Rhode Island": "RI", 
                "Colorado": "CO", "Minnesota": "MN", "South Carolina": "SC", 
                "Connecticut": "CT", "Mississippi": "MS", "South Dakota": "SD", 
                "Delaware": "DE", "Missouri": "MO", "Tennessee": "TN", 
                "District of Columbia": "DC", "Montana": "MT", 
                "Texas": "TX", "Florida": "FL", "Nebraska": "NE", 
                "Trust Territories": "TT", "Georgia": "GA", 
                "Nevada": "NV", "Utah": "UT", "Guam": "GU", 
                "New Hampshire": "NH", "NH	Vermont": "VT", "Hawaii": "HI", 
                "New Jersey": "NJ", "Virginia": "VA", "Idaho": "ID", 
                "New Mexico": "NM", "Virgin Islands": "VI", "Illinois": "IL", 
                "New York": "NY", "Washington": "WA", "Indiana": "IN",
                "North Carolina": "NC", "West Virginia": "WV", "Iowa": "IA", 
                "North Dakota": "ND", "Wisconsin": "WI", "Kansas": "KS", 
                "Northern Mariana Islands": "MP", "Wyoming": "WY"}
        
        url = "https://apps.fs.usda.gov/fia/datamart/CSV/{}_{}.csv"

            
        for state in states.values():
            download_path = f"{RAW_DIR}FIA/"
            if not os.path.exists(download_path):
                os.mkdir(download_path)
            for file in ['PLOT', 'TREE']:
                # URL of the CSV file
                print(f"Downloading {state}_{file} data")

                # Send a GET request to download the file
                response = requests.get(url, stream=True)

                # Check if the request was successful
                if response.status_code == 200:
                    # Save the content to a local file in chunks
                    with open(f"{download_path}/{state}_{file}.csv", "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:  # Filter out keep-alive chunks
                                f.write(chunk)
                    print(f"Download successful for {state}_{file}")
                else:
                    print(f"Failed to download file. Status code: {response.status_code} for {state}_{file}")



