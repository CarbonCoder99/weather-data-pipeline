from sqlalchemy import create_engine

# Replace [YOUR-PASSWORD] with your actual password
DB_URI = "postgresql://postgres:vsOHLeWizGp6eYer@db.mmbuabemfkxdavsaaccq.supabase.co:5432/postgres"

try:
    engine = create_engine(DB_URI)
    connection = engine.connect()
    print("🚀 SUCCESS: Python is talking to the Database!")
    connection.close()
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")