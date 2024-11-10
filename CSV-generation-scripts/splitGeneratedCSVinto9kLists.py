import pandas as pd

# Load the large CSV file
input_csv = 'facilities_with_real_address_info.csv'  # Replace with your actual file path

# Define chunk size (9000 rows per file)
chunk_size = 9000

# Read the large CSV in chunks
chunks = pd.read_csv(input_csv, chunksize=chunk_size)

# Split and save each chunk into a separate CSV file
for i, chunk in enumerate(chunks):
    # Create a filename for each chunk
    output_csv = f'split_file_{i+1}.csv'
    
    # Save the chunk to a new CSV file, including the header (column names)
    chunk.to_csv(output_csv, index=False)

    print(f'Saved {output_csv}')