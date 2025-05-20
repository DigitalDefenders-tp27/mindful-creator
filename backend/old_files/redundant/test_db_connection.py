import os
import psycopg2
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_postgres_connection():
    """Test connection to PostgreSQL database"""
    print("Testing PostgreSQL connection...")
    
    # Get DATABASE_URL from environment or use the provided hostname
    db_url = os.getenv("DATABASE_URL", "postgres-production-7575.up.railway.app")
    
    # Format connection string if it's just a hostname
    if "://" not in db_url:
        # Default to standard credentials for Railway
        connection_string = f"postgresql://postgres:postgres@{db_url}:5432/railway"
    else:
        # If it's already a full connection string, use it as is
        connection_string = db_url.replace("postgres://", "postgresql://")
    
    print(f"Using connection string format: {connection_string[:connection_string.find('@')+1]}****")
    
    try:
        # Try to connect to the database
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("Successfully connected to PostgreSQL database!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        # List tables in the database
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("\nTables in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("\nNo tables found in the database.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: Could not connect to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    success = test_postgres_connection()
    sys.exit(0 if success else 1) 