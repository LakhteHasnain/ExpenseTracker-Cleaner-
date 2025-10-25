"""
Migration 003: Create Token Blacklist Table

What this does:
- Creates token_blacklist table to store revoked tokens
- Prevents logout tokens from being used again
- Enables logout functionality

Why we need it:
- When user logs out, their token should be invalidated
- Prevents token reuse after logout
- Protects against token compromise

When to use:
- Run this AFTER migrations 001 and 002
- It's safe to run multiple times
"""

from sqlalchemy import text

def upgrade(engine):
    """
    UPGRADE = Create token_blacklist table
    
    This table stores:
    - token: The JWT token that was revoked
    - blacklisted_at: When the token was blacklisted
    - expires_at: When the token naturally expires
    """
    print("\n" + "="*60)
    print("MIGRATION 003: Creating Token Blacklist Table")
    print("="*60)
    
    try:
        with engine.connect() as connection:
            # Create token_blacklist table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS token_blacklist (
                    id SERIAL PRIMARY KEY,
                    token VARCHAR(500) UNIQUE NOT NULL,
                    blacklisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create index on token for faster lookups
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_token_blacklist_token ON token_blacklist(token)
            """))
            
            # Create index on expires_at for cleanup queries
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_token_blacklist_expires_at ON token_blacklist(expires_at)
            """))
            
            connection.commit()
            
            print("✓ Token blacklist table created successfully!")
            print("✓ Token index created for faster lookups!")
            print("✓ Expires_at index created for cleanup!")
            print("\nTable columns:")
            print("  • id (SERIAL) - Primary key")
            print("  • token (VARCHAR) - Revoked JWT token")
            print("  • blacklisted_at (TIMESTAMP) - When token was revoked")
            print("  • expires_at (TIMESTAMP) - When token naturally expires")
            print("  • created_at (TIMESTAMP) - When record was created")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error creating token blacklist table: {str(e)}")
        raise

def downgrade(engine):
    """
    DOWNGRADE = Delete token_blacklist table
    
    WARNING: This will remove all blacklisted token records!
    Only use this if you need to undo this migration.
    """
    print("\n" + "="*60)
    print("MIGRATION 003: Rolling Back - Deleting Token Blacklist Table")
    print("="*60)
    print("⚠️  WARNING: This will DELETE all blacklisted token records!\n")
    
    try:
        with engine.connect() as connection:
            # Drop the token_blacklist table
            connection.execute(text("DROP TABLE IF EXISTS token_blacklist CASCADE"))
            connection.commit()
            
            print("✓ Token blacklist table deleted successfully!")
            print("✓ All blacklisted token records have been removed")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"✗ Error deleting token blacklist table: {str(e)}")
        raise
