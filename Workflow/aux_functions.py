
import pandas as pd
import numpy as np
import umap
import sys
import os

#Simple yes or no input function (default NO)
def yes_or_NO(question):
    while True:
        reply = str(input(question+' (y/[n]): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        elif reply[:1] == 'n':
            return False
        elif reply[:1] == "":
            return False
        else:
            print ("Please answer Y or N")

#Function to concatenate all files
def concatenate_fcs(folder_name):
    input_files = [f for f in os.listdir(f"./{folder_name}") if f.endswith(".txt")]
    no_arc = pd.DataFrame()
    #Add counter to keep track of the number of files in input -> 
    # -> cell ID will be a mix of these (Filenumber | filename.txt)
    fcounter = 0
    for file in input_files:
        fcounter += 1
        df = pd.read_csv(f"{folder_name}/{file}", sep = '\t')
        df["file_origin"] = str(fcounter)+" | "+ file # add a new column of 'file_origin' that will be used to separate each file after umap calculation
        df["Sample_ID-Cell_Index"] = df["Cell_Index"].apply(lambda x: str(fcounter)+"-"+str(x)) #File+ID #This way the cell-index will be preserved after Cytobank upload
        # df["Cell_Index"] = df["Cell_Index"].apply(lambda x: str(fcounter)+"-"+str(x)) #File+ID
        no_arc = no_arc.append(df, ignore_index=True)
    return no_arc

#Arcsinh transform the data
def arcsinh_transf(cofactor, no_arc):
    #Select only the columns containing the markers (as they start with a number for the isotope)
    cols = [x for x in no_arc.columns if x[0].isdigit()]
    #Apply the arcsinh only to those columns (don't want to change time or any other)
    arc = no_arc.apply(lambda x: np.arcsinh(x/cofactor) if x.name in cols else x)
    # put back the 'file_origin' column to the arcsinh-transformed data
    if "file_origin" in  no_arc.columns:
        arc["file_origin"] = no_arc["file_origin"]
    # else:
    #     print ("(there was no concatenation prior to transforming)")
    return arc, cols

# Random downsampling of a dataframe to n rows
def downsample_df(df, n):
    df_downsampled = df.sample(n)
    return df_downsampled

#Function to concatenate all files and save as txt 
def concatenate_save(folder_name):
    input_files = [f for f in os.listdir(f"./{folder_name}") if f.endswith(".txt")]
    concat = pd.DataFrame()
    #Add counter to keep track of the number of files in input -> 
    # -> cell ID will be a mix of these (Filenumber | filename.txt)
    fcounter = 0
    for file in input_files:
        name = file.split('.txt')[0]
        fcounter += 1
        df = pd.read_csv(f"{folder_name}/{file}", sep = '\t')
        df["file_origin"] = str(fcounter)+" | "+ file # add a new column of 'file_origin' that will be used to separate each file after umap calculation
        df["Sample_ID-Cell_Index"] = df["Cell_Index"].apply(lambda x: str(fcounter)+"-"+str(x)) #File+ID #This way the cell-index will be preserved after Cytobank upload
        # df["Cell_Index"] = df["Cell_Index"].apply(lambda x: str(fcounter)+"-"+str(x)) #File+ID
        concat = concat.append(df, ignore_index=True)

    print("Concatenating...")
    concat.to_csv(f'./output/opt1_concatenation/concat_{name}.txt', index = False, sep = '\t')
    print(f"Concatenated file saved as:\nconcat_{name}.txt")