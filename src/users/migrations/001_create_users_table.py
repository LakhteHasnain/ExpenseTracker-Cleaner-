"""
Migration 001: Create Users Table

What this does:
- Creates a 'users' table in your database
- This table stores user information (name, email, password)

When to use:
- Run this ONCE when setting up your project
- It's safe to run multiple times (won't create duplicates)
"""

from sqlalchemy import text

def upgrade(engine):
    """
    UPGRADE = Apply the migration (CREATE the table)
    
    This function creates the users table with the following columns:
    - user_id: Unique identifier (UUID)
    - name: User's full name (max 100 characters)
    - email: User's email (unique, max 100 characters)
    - password: Hashed password (max 255 characters)
    - created_at: Timestamp when user was created
    """
    print("\n" + "="*60)
    print("MIGRATION 001: Creating Users Table")
    print("="*60)
    
    try:
        with engine.connect() as connection:
            # SQL command to create the table
            sql = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            connection.execute(text(sql))
            
            # Also create an index on email for faster searches
            connection.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"
            ))
            
            connection.commit()
            
            print("✓ Users table created successfully!")
            print("✓ Email index created for faster searches!")
            print("\nTable columns:")
            print("  • user_id (UUID) - Unique user identifier")
            print("  • name (VARCHAR) - User's full name")
            print("  • email (VARCHAR) - User's email (unique)")
            print("  • password (VARCHAR) - Hashed password")
            print("  • created_at (TIMESTAMP) - When user was created")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error creating table: {str(e)}")
        raise

def downgrade(engine):
    """
    DOWNGRADE = Undo the migration (DELETE the table)
    
    WARNING: This will delete all user data!
    Only use this if you need to start over.
    """
    print("\n" + "="*60)
    print("MIGRATION 001: Rolling Back - Deleting Users Table")
    print("="*60)
    print("⚠️  WARNING: This will DELETE all user data!\n")
    
    try:
        with engine.connect() as connection:
            # SQL command to delete the table
            connection.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            connection.commit()
            
            print("✓ Users table deleted successfully!")
            print("✓ All user data has been removed")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error deleting table: {str(e)}")
        raise
