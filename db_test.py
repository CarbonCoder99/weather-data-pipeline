from sqlalchemy import create_engine

# Try the new password here
# Note the 'postgresql' at the start!
DB_URI = "postgresql://postgres:WeatherData2026@db.mbuabemfkxdavsaaccq.supabase.co:5432/postgres"

try:
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        print("✅ CONNECTION SUCCESSFUL!")
except Exception as e:
    print(f"❌ ERROR: {e}")