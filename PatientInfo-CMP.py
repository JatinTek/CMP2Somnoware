# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 19:50:05 2024

@author: rache
"""

import os
import xml.etree.ElementTree as ET
import pandas as pd
import time


def find_xml_files(root_dir, filename="STUDYCFG.XML"):
    """Find all XML files with the specified filename in all subdirectories of the given root directory."""
    xml_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.upper() == filename.upper():
                xml_files.append(os.path.join(root, file))
    return xml_files

def parse_xml_to_df(xml_files):
    """Parse the specified XML files and return a dataframe with the required information."""
    data = []
    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        # Assuming the structure is: <PSGStudyConfig><Surname>...</Surname><GivenName>...</GivenName>...</PSGStudyConfig>
        last_name = root.find('.//Surname').text
        first_name = root.find('.//GivenName').text
        dob = root.find('.//DOB').text
        dos = root.find('.//StartDate').text
        data.append({'Last_Name': last_name, 'First_name': first_name, 'DOB': dob, 'DOS': dos})
    return pd.DataFrame(data)


# completed directory, comment out after testing
root_dir = "C:\\ProgramData\\Somnoware Healthcare Systems\\TechClient\\Somnoware\\Scoring_App\\Scored_studies\\Kell West"

#comment this line to allow for testing, using old data
#root_dir = "C:\\Users\\rache\\OneDrive\\Score\\Studies2Score\\Kell West"


# Find all relevant XML files
xml_files = find_xml_files(root_dir)

# Parse XML files and create dataframe
df = parse_xml_to_df(xml_files)

# Display the dataframe
print(df)

import pandas as pd
from datetime import datetime

def calculate_age(dob, dos):
    """Calculate age given dob and dos in MM/DD/YYYY format."""
    dob = datetime.strptime(dob, "%d/%m/%Y")
    dos = datetime.strptime(dos, "%d/%m/%Y")
    age = dos.year - dob.year - ((dos.month, dos.day) < (dob.month, dob.day))
    return age

def transform_dataframe(df):
    """Transform the input dataframe as per the requirements."""
    # Concatenate Last_Name and First_Name to create Full_Name
    df['Full_Name'] = df['Last_Name'] + ", " + df['First_name']
    
    # Calculate Age based on DOB and DOS
    df['Age'] = df.apply(lambda row: calculate_age(row['DOB'], row['DOS']), axis=1)
    
    # Select and reorder the required columns
    output_df = df[['Full_Name', 'DOB', 'Age', 'DOS']]
    output_df['DOB'] = output_df['DOB'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%m/%d/%Y'))
    output_df['DOS'] = output_df['DOS'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%m/%d/%Y'))
    return output_df




output_df = transform_dataframe(df)
print(output_df)



# copy dataFrame to clipboard
output_df.to_clipboard(excel=True, sep=None, index=False, header=None)

