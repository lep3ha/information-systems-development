from app.db.context_manager import DBContextManager

try:
    with DBContextManager() as db:
        db.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'supplier' ORDER BY ordinal_position")
        print('=== supplier ===')
        for row in db.fetchall():
            print(f"{row[0]}: {row[1]}")
        
        db.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'delivery' ORDER BY ordinal_position")
        print('\n=== delivery ===')
        for row in db.fetchall():
            print(f"{row[0]}: {row[1]}")
        
        db.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'delivery_item' ORDER BY ordinal_position")
        print('\n=== delivery_item ===')
        for row in db.fetchall():
            print(f"{row[0]}: {row[1]}")
except Exception as e:
    print(f"Error: {e}")
