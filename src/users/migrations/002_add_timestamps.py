"""
Migration 002: Add Timestamps to Users Table

What this does:
- Adds created_at column (when user was created)
- Adds updated_at column (when user was last updated)

Why we need it:
- Track when users sign up
- Track when user information is modified
- Useful for auditing and debugging

When to use:
- Run this AFTER migration 001
- It's safe to run multiple times
"""

from sqlalchemy import text

def upgrade(engine):
    """
    UPGRADE = Add timestamp columns to users table
    
    This adds two new columns:
    - created_at: Automatically set when user is created
    - updated_at: Automatically updated when user data changes
    """
    print("\n" + "="*60)
    print("MIGRATION 002: Adding Timestamps to Users Table")
    print("="*60)
    
    try:
        with engine.connect() as connection:
            # Add created_at column if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """))
                print("✓ created_at column added")
            except Exception as e:
                if "already exists" in str(e):
                    print("✓ created_at column already exists")
                else:
                    raise
            
            # Add updated_at column if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """))
                print("✓ updated_at column added")
            except Exception as e:
                if "already exists" in str(e):
                    print("✓ updated_at column already exists")
                else:
                    raise
            
            connection.commit()
            
            print("\nNew columns added:")
            print("  • created_at (TIMESTAMP) - When user was created")
            print("  • updated_at (TIMESTAMP) - When user was last updated")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error adding timestamps: {str(e)}")
        raise

def downgrade(engine):
    """
    DOWNGRADE = Remove timestamp columns from users table
    
    WARNING: This will remove the timestamp columns!
    Only use this if you need to undo this migration.
    """
    print("\n" + "="*60)
    print("MIGRATION 002: Rolling Back - Removing Timestamps")
    print("="*60)
    print("⚠️  WARNING: This will REMOVE timestamp columns!\n")
    
    try:
        with engine.connect() as connection:
            # Remove created_at column
            try:
                connection.execute(text("""
                    ALTER TABLE users
                    DROP COLUMN IF EXISTS created_at
                """))
                print("✓ created_at column removed")
            except Exception as e:
                print(f"✓ created_at column already removed or doesn't exist")
            
            # Remove updated_at column
            try:
                connection.execute(text("""
                    ALTER TABLE users
                    DROP COLUMN IF EXISTS updated_at
                """))
                print("✓ updated_at column removed")
            except Exception as e:
                print(f"✓ updated_at column already removed or doesn't exist")
            
            connection.commit()
            
            print("\nTimestamp columns removed")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error removing timestamps: {str(e)}")
        raise