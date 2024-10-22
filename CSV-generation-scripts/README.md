# GeoJSON Parser and CSV Splitter

## Overview
This repository contains two Python scripts for parsing GeoJSON data and splitting large CSV files for easy upload:

1. `parseGeojsonAndGenerateCSV.py`: Parses a GeoJSON file and generates a CSV with real addresses.
2. `splitGeneratedCSVinto9kLists.py`: Splits a large CSV file into smaller chunks to facilitate easier uploads (e.g., via AWS).

## Script 1: GeoJSON to CSV Parser

### Description
The script `parseGeojsonAndGenerateCSV.py` parses a GeoJSON file and generates a CSV file with:
- A randomized name starting with "Test - " followed by three random words from a predefined list.
- Real addresses parsed from the GeoJSON file.

### Example
In this example, we use `calgary-addresses-city.geojson` to create one large CSV file.

### Instructions

1. **Download GeoJSON File**: 
   - Go to [OpenAddresses](https://batch.openaddresses.io/) and download the desired GeoJSON file.

2. **Set GeoJSON File Path**: 
   - Modify line 105 of the script to specify the GeoJSON file you wish to parse:
     ```python
     geojson_file_path = 'calgary-addresses-city-full.geojson'
     ```

3. **Run the Script**: 
   - Place the `parseGeojsonAndGenerateCSV.py` script and the GeoJSON file (e.g., `calgary-addresses-city.geojson`) in the same folder.
   - Run the following command in your terminal:
     ```bash
     python3 parseGeojsonAndGenerateCSV.py
     ```
   - The script will generate a CSV file containing parsed addresses.

### Output
The output will be a CSV file. Note that the generated CSV may contain more than 10,000 records, which could cause issues during file uploads due to AWS limitations.

---

## Script 2: CSV Splitter

### Description
The script `splitGeneratedCSVinto9kLists.py` splits a large CSV file into smaller files, each containing 9,000 records. This helps avoid issues during uploads, especially if there are AWS limits on file size or record count.

### Instructions

1. **Modify the Input File Path**: 
   - Update line 4 of the script to specify the name and path of the generated CSV file:
     ```python
     input_csv = 'calgary_facilities_with_country_info_TestNazarNafisa.csv'
     ```

2. **Run the Script**: 
   - Place the `splitGeneratedCSVinto9kLists.py` script and the large CSV file in the same folder.
   - Run the following command in your terminal:
     ```bash
     python3 splitGeneratedCSVinto9kLists.py
     ```

### Output
The script will generate multiple CSV files, each containing up to 9,000 records, making them suitable for upload.

---

## Notes

- It's recommended to split CSV files into 9,000 records instead of 10,000 to avoid issues where AWS may fail to process files due to duplicate records or limits on the number of rows processed.
- Ensure that the generated CSV file is in the same folder as the splitting script before running it.


