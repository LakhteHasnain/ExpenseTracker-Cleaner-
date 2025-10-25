"""
Migration runner for users module

What is a migration?
- A migration is a file that describes changes to your database
- Each migration has two functions:
  1. upgrade() - Creates/modifies tables (runs when you want to apply changes)
  2. downgrade() - Removes/reverts changes (runs when you want to undo)

How it works:
1. You create a migration file (e.g., 001_create_users_table.py)
2. You run the migration to apply changes to the database
3. If something goes wrong, you can rollback (undo) the migration
"""

from sqlalchemy import text

class MigrationRunner:
    def __init__(self, engine):
        self.engine = engine
    
    def run_all_migrations(self):
        """
        Run ALL migrations in order
        
        This runs:
        1. Migration 001: Create users table
        2. Migration 002: Add timestamps
        
        Safe to run multiple times!
        """
        print("\n" + "#"*60)
        print("# RUNNING ALL MIGRATIONS")
        print("#"*60)
        
        # Import migrations using sys.path
        import sys
        import os
        from pathlib import Path
        
        migrations_dir = Path(__file__).parent
        sys.path.insert(0, str(migrations_dir))
        
        try:
            # Import migration modules by their file names
            import importlib.util
            
            migration_files = [
                ("001", "001_create_users_table.py"),
                ("002", "002_add_timestamps.py"),
                ("003", "003_create_token_blacklist.py"),
            ]
            
            for migration_num, filename in migration_files:
                filepath = migrations_dir / filename
                spec = importlib.util.spec_from_file_location(f"migration_{migration_num}", filepath)
                migration_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration_module)
                
                try:
                    print(f"\n[{migration_num}] Running migration...")
                    migration_module.upgrade(self.engine)
                except Exception as e:
                    print(f"\n[{migration_num}] Error: {str(e)}")
                    print("Stopping migration process...")
                    break
        finally:
            sys.path.pop(0)
        
        print("\n" + "#"*60)
        print("# ALL MIGRATIONS COMPLETED")
        print("#"*60 + "\n")
    
    def run_migration(self):
        """
        DEPRECATED: Use run_all_migrations() instead
        
        This is kept for backwards compatibility
        """
        print("\n" + "="*60)
        print("STEP 1: Creating Users Table")
        print("="*60)
        
        try:
            with self.engine.connect() as connection:
                # Create users table
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create index on email for faster lookups
                connection.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
                """))
                
                connection.commit()
                print("✓ Users table created successfully!")
                print("✓ Email index created for faster searches!")
                print("\nTable Structure:")
                print("  - user_id: Unique identifier (UUID)")
                print("  - name: User's full name (max 100 characters)")
                print("  - email: User's email (unique, max 100 characters)")
                print("  - password: Hashed password (max 255 characters)")
                print("  - created_at: When the user was created")
                print("  - updated_at: When the user was last updated")
        except Exception as e:
            print(f"✗ Error creating table: {str(e)}")
    
    def rollback_migration(self):
        """
        DEPRECATED: Use rollback_all_migrations() instead
        
        Deletes the users table (undo changes)
        WARNING: This will delete all user data!
        """
        print("\n" + "="*60)
        print("STEP 2: Rolling Back - Deleting Users Table")
        print("="*60)
        print("⚠️  WARNING: This will DELETE all user data!")
        
        try:
            with self.engine.connect() as connection:
                # Drop the users table
                connection.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                connection.commit()
                print("✓ Users table deleted successfully!")
                print("✓ All user data has been removed")
        except Exception as e:
            print(f"✗ Error deleting table: {str(e)}")
    
    def rollback_all_migrations(self):
        """
        Rollback ALL migrations in reverse order
        
        This undoes:
        2. Migration 002: Remove timestamps
        1. Migration 001: Delete users table
        
        WARNING: This will DELETE all user data!
        """
        print("\n" + "#"*60)
        print("# ROLLING BACK ALL MIGRATIONS")
        print("#"*60)
        print("⚠️  WARNING: This will DELETE all user data!\n")
        
        # Import migrations in reverse order
        import sys
        from pathlib import Path
        import importlib.util
        
        migrations_dir = Path(__file__).parent
        sys.path.insert(0, str(migrations_dir))
        
        try:
            migration_files = [
                ("003", "003_create_token_blacklist.py"),
                ("002", "002_add_timestamps.py"),
                ("001", "001_create_users_table.py"),
            ]
            
            for migration_num, filename in migration_files:
                filepath = migrations_dir / filename
                spec = importlib.util.spec_from_file_location(f"migration_{migration_num}", filepath)
                migration_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration_module)
                
                try:
                    print(f"\n[{migration_num}] Rolling back migration...")
                    migration_module.downgrade(self.engine)
                except Exception as e:
                    print(f"\n[{migration_num}] Error: {str(e)}")
                    print("Stopping rollback process...")
                    break
        finally:
            sys.path.pop(0)
        
        print("\n" + "#"*60)
        print("# ALL MIGRATIONS ROLLED BACK")
        print("#"*60 + "\n")
