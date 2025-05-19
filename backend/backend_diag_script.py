import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import json

def run_diagnostics():
    """
    Runs diagnostic tests on the backend's database connection and table structures.
    """
    db_url = os.environ.get("DATABASE_PUBLIC_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set.")
        return

    print(f"Attempting to connect to database with URL: {db_url[:db_url.find('@') + 1]}********") # Mask credentials

    try:
        # Correct handling for 'postgres://' prefix if SQLAlchemy < 1.4 and URL is for PostgreSQL
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            print("\n--- Database Connection Test ---")
            print("Successfully connected to the database.")

            inspector = inspect(engine)

            print("\n--- Accessible Tables ---")
            all_tables = inspector.get_table_names()
            if all_tables:
                print("Found tables:")
                for table_name in all_tables:
                    print(f"- {table_name}")
            else:
                print("No tables found by the inspector.")

            # Specific checks for train_cleaned
            print("\n--- Table: train_cleaned ---")
            if "train_cleaned" in all_tables:
                print("train_cleaned table IS accessible.")
                try:
                    columns = inspector.get_columns("train_cleaned")
                    if columns:
                        print("Columns found in train_cleaned:")
                        for column in columns:
                            print(f"- Name: {column['name']}, Type: {column['type']}")
                    else:
                        print("No columns found for train_cleaned (inspector.get_columns returned empty).")
                    
                    print("\nAttempting to query train_cleaned (LIMIT 5):")
                    query_train = text("SELECT * FROM train_cleaned LIMIT 5")
                    result_train = connection.execute(query_train)
                    rows_train = result_train.fetchall()
                    if rows_train:
                        print(f"Successfully fetched {len(rows_train)} row(s) from train_cleaned.")
                        # for row in rows_train:
                        #     print(dict(row._mapping)) # Python 3.x way for RowProxy
                    else:
                        print("Query executed but returned no rows from train_cleaned.")
                except SQLAlchemyError as e_query_train:
                    print(f"Error querying train_cleaned or getting its columns: {e_query_train}")
                except Exception as e_inspect_train:
                    print(f"Unexpected error inspecting train_cleaned: {e_inspect_train}")

            else:
                print("train_cleaned table IS NOT accessible or does not exist in the default search path.")

            # Specific checks for smmh_cleaned
            print("\n--- Table: smmh_cleaned ---")
            if "smmh_cleaned" in all_tables:
                print("smmh_cleaned table IS accessible.")
                try:
                    columns_smmh = inspector.get_columns("smmh_cleaned")
                    if columns_smmh:
                        print("Columns found in smmh_cleaned:")
                        for column in columns_smmh:
                            print(f"- Name: {column['name']}, Type: {column['type']}")
                    else:
                        print("No columns found for smmh_cleaned (inspector.get_columns returned empty).")

                    print("\nAttempting to query smmh_cleaned (LIMIT 5):")
                    # For tables with potentially problematic column names, quote the table name.
                    # And select specific, known-simple columns if possible, or use try-except for SELECT *
                    try:
                        query_smmh = text('SELECT "Timestamp", "2. Gender" FROM smmh_cleaned LIMIT 5') # Example with quoted known columns
                        # If you want to try SELECT *, be prepared for errors if column names are too weird for default mapping
                        # query_smmh = text('SELECT * FROM "smmh_cleaned" LIMIT 5') 
                        result_smmh = connection.execute(query_smmh)
                        rows_smmh = result_smmh.fetchall()
                        if rows_smmh:
                            print(f"Successfully fetched {len(rows_smmh)} row(s) from smmh_cleaned.")
                            # for row in rows_smmh:
                            #     print(dict(row._mapping))
                        else:
                            print("Query executed but returned no rows from smmh_cleaned.")
                    except SQLAlchemyError as e_select_smmh:
                        print(f"Error executing SELECT on smmh_cleaned: {e_select_smmh}")
                        print("This might be due to complex column names. Try selecting specific columns with quotes.")

                except SQLAlchemyError as e_query_smmh:
                    print(f"Error querying smmh_cleaned or getting its columns: {e_query_smmh}")
                except Exception as e_inspect_smmh:
                    print(f"Unexpected error inspecting smmh_cleaned: {e_inspect_smmh}")
            else:
                print("smmh_cleaned table IS NOT accessible or does not exist in the default search path.")

            print("\n--- End of Diagnostics ---")

    except SQLAlchemyError as e_connect:
        print(f"ERROR: Database connection failed or SQLAlchemy operation error: {e_connect}")
    except Exception as e_general:
        print(f"An unexpected error occurred: {e_general}")

if __name__ == "__main__":
    run_diagnostics() 