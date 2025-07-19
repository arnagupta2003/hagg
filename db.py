import psycopg2
import json
import os

# Database connection details
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_NAME = 'hagg'  # You can change this if your database has a different name
DB_USER = 'postgres'  # <--- IMPORTANT: Replace with your PostgreSQL username
DB_PASSWORD = 'postgres'  # <--- IMPORTANT: Replace with your PostgreSQL password

# Path to your out.txt file
OUT_FILE_PATH = 'out.txt' # Make sure out.txt is in the same directory, or provide full path

def read_data_from_file(file_path):
    """
    Reads data from the specified file, assuming each listing is separated by '====..==='.
    Parses each listing as a JSON object.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        data_string = f.read()

    listings_raw = data_string.strip().split("====..===")
    parsed_data = []
    for listing_str in listings_raw:
        if listing_str.strip(): # Ensure it's not an empty string
            try:
                parsed_data.append(json.loads(listing_str.strip()))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e} in string: {listing_str.strip()[:200]}...") # Print first 200 chars for context
    return parsed_data

def create_table_and_insert_data(data_entries):
    """
    Connects to the PostgreSQL database, creates the 'listings' table if it doesn't exist,
    and inserts the provided data entries.
    """
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        # Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS listings (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            society_name VARCHAR(255),
            society_url TEXT,
            posted_date VARCHAR(50),
            summary JSONB,
            rent_price INTEGER,
            description TEXT,
            agent_name VARCHAR(255),
            operating_since VARCHAR(50),
            json_ld JSONB
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'listings' checked/created successfully.")

        # Insert data
        insert_query = """
        INSERT INTO listings (
            title, society_name, society_url, posted_date, summary,
            rent_price, description, agent_name, operating_since, json_ld
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON CONFLICT (id) DO NOTHING; -- Added ON CONFLICT to avoid errors if primary key 'id' conflicts (though SERIAL should prevent this)
        """

        for entry in data_entries:
            try:
                # Convert rent_price to integer if it's a string
                # Remove commas from rent_price if present
                rent_price = int(entry.get("rent_price").replace(",", "")) if entry.get("rent_price") else None

                cur.execute(insert_query, (
                    entry.get("title"),
                    entry.get("society_name"),
                    entry.get("society_url"),
                    entry.get("posted_date"),
                    json.dumps(entry.get("summary")),  # Convert dict to JSON string for JSONB
                    rent_price,
                    entry.get("description"),
                    entry.get("agent_name"),
                    entry.get("operating_since"),
                    json.dumps(entry.get("json_ld"))  # Convert dict to JSON string for JSONB
                ))
                print(f"Inserted data for: {entry.get('title')}")
            except Exception as e:
                print(f"Error inserting data for entry: {entry.get('title')}. Error: {e}")
                conn.rollback() # Rollback on individual entry error
                continue # Continue to the next entry

        conn.commit()
        print("All data insertion attempts completed.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    print(f"Attempting to read data from {OUT_FILE_PATH}")
    parsed_data = read_data_from_file(OUT_FILE_PATH)

    if parsed_data:
        print(f"Successfully read {len(parsed_data)} listings from {OUT_FILE_PATH}.")
        create_table_and_insert_data(parsed_data)
    else:
        print("No data was parsed. Please check the file content and path.")