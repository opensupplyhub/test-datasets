import json
import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor

# List of unique facility types
facility_types = ['Industrial', 'Commercial', 'Agricultural', 'Residential']

# List of unique processing types
processing_types = ['Recycling', 'Manufacturing', 'Warehousing', 'Logistics']

# List of sectors
sectors = [ "Electronics", "Accommodation", "Aerospace", "Agriculture", "Air Transportation", "Allied Products", "Animal Production",
    "Apparel", "Apparel Accessories", "Appliances", "Aquaculture", "Archives", "Arts", "Arts & Entertainment", "Automotive",
    "Automotive Parts", "Banking", "Beauty Products", "Beverages", "Biotechnology", "Books", "Building Construction", 
    "Building Materials", "Chemicals", "Civics", "Civil Engineering Construction", "Coal", "Commodities", "Components", 
    "Computers", "Computing Infrastructure", "Construction", "Consumer Products", "Crop Production", "Durable Goods", 
    "Educational Services", "Electrical Devices", "Electricity", "Electronic Product Manufacturing", "Energy", 
    "Energy Production & Utilities", "Entertainment", "Equipment", "Farming", "Finance", "Financial Services", "Fishing", 
    "Food", "Food & Beverage", "Food Industry", "Food Manufacturing", "Footwear", "Forestry", "Furniture", "Garden Tools", 
    "Gas", "General Merchandise", "Ground Passenger Transportation", "Hard Goods", "Health", "Healthcare", "Hobby", 
    "Home Accessories", "Home Furnishings", "Hospitals", "Home Textiles", "Hunting", "Information", "International Affairs", 
    "Jewelry", "Leather", "Logging", "Machinery Manufacturing", "Maintenance", "Manufacturing", "Material Production", 
    "Medical Equipment & Services", "Merchant Wholesalers", "Metal Manufacturing", "Mining", "Multi-Category", 
    "Musical Instruments", "Nondurable Goods", "Nursing", "Oil & Gas", "Paper Products", "Parts Dealers", 
    "Personal Care Products", "Pharmaceuticals", "Pipeline Transportation", "Plastics", "Printing", "Professional Services", 
    "Quarrying", "Rail Transportation", "Recreation", "Renewable Energy", "Renting", "Repair", "Rubber Products", 
    "Solar Energy", "Research", "Specialty Trade Contractors", "Sports Equipment", "Sporting Goods", "Storage", 
    "Supplies Dealers", "Technical Services", "Technology", "Telecommunications", "Textiles", "Tobacco Products", "Toys", 
    "Transportation Equipment", "Trucking", "Utilities", "Water Utilities", "Warehousing", "Wholesale Trade", "Wood Products", 
    "Consumer Electronics", "Home", "Maritime Transportation", "Technical and Scientific Activities", "Waste Management", 
    "Recycling"
]

# Large word list for random names
words = [
    "Rapid", "Ocean", "Mountain", "River", "Sky", "Thunder", "Bliss", "Forest", "Storm", "Valley", "Bright", "Stone",
    "Leaf", "Cloud", "Fire", "Ice", "Wind", "Sun", "Snow", "Rain", "Flame", "Shadow", "Light", "Moon", "Star", "Echo", 
    "Peak", "Whisper", "Frost", "Glare", "Rock", "Stream", "Fog", "Lightning", "Moss", "Creek", "Hill", "Cave", 
    "Meadow", "Dawn", "Dusk", "Gale", "Wave", "Blaze", "Tempest", "Zephyr", "Aurora", "Breeze", "Cliff", "Glacier", 
    "Grove", "Horizon", "Tide", "Cascade", "Chill", "Twilight", "Mist", "Prairie", "Ridge", "Summit", "Tornado", 
    "Volcano", "Woods", "Harbor", "Lagoon", "Pond", "Desert", "Oasis", "Ravine", "Sand", "Boulder", "Crater", 
    "Estuary", "Harsh", "Savanna", "Steppe", "Swamp", "Tundra", "Canyon", "Delta", "Gulf", "Pass", "Plateau", 
    "Quarry", "Rainforest", "Savannah", "Shore", "Slope", "Bay", "Dune", "Coral", "Isle", "Reef", "Spruce", "Elm", 
    "Birch", "Pine", "Fir", "Maple", "Cedar", "Oak", "Cypress", "Sequoia", "Willow", "Hazel", "Hickory", "Beech", 
    "Aspen", "Redwood", "Magnolia", "Bramble", "Hemlock", "Ivy", "Juniper", "Myrtle", "Palm", "Yew", "Bamboo", 
    "Mahogany", "Rosewood", "Teak", "Walnut", "Acacia", "Alder", "Aloe", "Baobab", "Chestnut", "Dogwood", 
    "Elder", "Ginkgo", "Hawthorn", "Laurel", "Mulberry", "Poplar", "Rowan", "Sassafras", "Tamarind", "Amaranth", 
    "Bracken", "Clover", "Dandelion", "Fern", "Lavender", "Mistletoe", "Nettle", "Saffron", "Sage", "Thyme", "Violet", 
    "Zinnia", "Aspen", "Azalea", "Buttercup", "Carnation", "Daisy", "Foxglove", "Geranium", "Hibiscus", 
    "Iris", "Jasmine", "Lilac", "Marigold", "Orchid", "Peony", "Poppy", "Rose", "Sunflower", "Tulip", 
    "Wisteria", "Acorn", "Berry", "Cactus", "Earth", "Fawn", "Grove", "Hill", "Inlet", "Jungle", 
    "Knoll", "Pebble", "Quartz", "Tundra", "Vale", "Wander", "Xylo", "Zephyr", "Antelope", "Bear", "Cougar", "Deer", 
    "Eagle", "Falcon", "Gorilla", "Hawk", "Jaguar", "Koala", "Leopard", "Moose", "Narwhal", "Ocelot", "Panda", "Seal", 
    "Tiger", "Ursa", "Viper", "Wolf", "Yak", "Zebra", "Amber", "Bronze", "Copper", "Diamond", "Emerald", "Flint", 
    "Gold", "Hematite", "Ivory", "Jade", "Kyanite", "Lapis", "Malachite", "Nickel", "Opal", "Pearl", "Quartz", 
    "Ruby", "Sapphire", "Topaz", "Zircon", "Azure", "Beige", "Charcoal", "Dandelion", "Ebony", "Fuchsia", "Gray", 
    "Heliotrope", "Indigo", "Khaki", "Lilac", "Magenta", "Navy", "Olive", "Peach", "Silver", "Taupe", 
    "Ultramarine", "Yellow", "Alabaster", "Buff", "Carmine", "Denim", "Emerald", "Flame", "Honey", 
    "Ivory", "Kiwi", "Lemon", "Mustard", "Onyx", "Plum", "Redwood", "Saffron", "Tangerine", "Verdant", 
    "Amethyst", "Burgundy", "Citrine", "Daffodil", "Emerald", "Feldspar", "Hickory", "Jasper", "Kale", "Lime", 
    "Mulberry", "Nutmeg", "Obsidian", "Periwinkle", "Quartz", "Raspberry" ]
   

# Random facility name generator (3 random words)
def generate_random_facility_name():
    return f"Test - {random.choice(words)} {random.choice(words)} {random.choice(words)}"

# Function to randomly assign facility_type and processing_type
def generate_random_facility_and_processing():
    facility_type = random.choice(facility_types)
    processing_type = random.choice(processing_types)
    return facility_type, processing_type

# Function to process a chunk of lines
def process_chunk(lines):
    records = []
    for line in lines:
        feature = json.loads(line.strip())
        number = feature['properties'].get('number', '')
        street = feature['properties'].get('street', '')
        city = "Calgary"
        country_code = "CA"  # Country code set to CA
        country_name = "Canada"  # Country name set to Canada
        address = f"{number} {street}, {city}"
        sector = random.choice(sectors)
        facility_name = generate_random_facility_name()

        # Assign random facility_type and processing_type
        facility_type, processing_type = generate_random_facility_and_processing()

        records.append({
            "name": facility_name,
            "address": address,
            "country": country_code,
            "country_name": country_name,
            "sector": sector,
            "facility_type": facility_type,
            "processing_type": processing_type
        })
    return records

# Main function to read and split the GeoJSON file and use multithreading
def main():
    geojson_file_path = 'calgary-addresses-city.geojson'
    
    # Read the entire file into memory
    with open(geojson_file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) == 0:
        print("Error: The file is empty.")
        return

    if len(lines) < 4:
        # If there are fewer than 4 lines, process all lines in one chunk
        chunks = [lines]
    else:
        # Split the lines into chunks for each thread (4 threads)
        chunk_size = max(1, len(lines) // 4)  # Ensure chunk_size is at least 1
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    # Use ThreadPoolExecutor to process chunks in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_chunk, chunks)

    # Combine all results into a single list
    all_records = []
    for result in results:
        all_records.extend(result)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_records)
    df.to_csv('facilities_with_real_address_info.csv', index=False)

    print(f"CSV file 'facilities_with_real_address_info.csv' created successfully!")

if __name__ == "__main__":
    main()
