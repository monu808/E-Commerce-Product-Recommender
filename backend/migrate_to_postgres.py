"""
Migrate data from SQLite to PostgreSQL on Render
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Product, Interaction, Base

def migrate_data():
    """Copy all data from SQLite to PostgreSQL"""
    
    # Source (SQLite - local)
    sqlite_engine = create_engine("sqlite:///./ecommerce.db")
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    
    # Destination (PostgreSQL - from environment)
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url:
        print("❌ ERROR: DATABASE_URL environment variable not set!")
        print("Set it with your PostgreSQL connection string")
        return
    
    print(f"Connecting to PostgreSQL...")
    postgres_engine = create_engine(postgres_url, pool_pre_ping=True)
    PostgresSession = sessionmaker(bind=postgres_engine)
    
    # Create tables in PostgreSQL
    print("Creating tables...")
    Base.metadata.create_all(postgres_engine)
    print("✓ Tables created")
    
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()
    
    try:
        # Migrate Users
        print("\nMigrating users...")
        users = sqlite_session.query(User).all()
        for user in users:
            # Check if user already exists
            existing = postgres_session.query(User).filter(User.id == user.id).first()
            if not existing:
                new_user = User(id=user.id, name=user.name)
                postgres_session.add(new_user)
        postgres_session.commit()
        print(f"✓ Migrated {len(users)} users")
        
        # Migrate Products
        print("Migrating products...")
        products = sqlite_session.query(Product).all()
        for product in products:
            existing = postgres_session.query(Product).filter(Product.id == product.id).first()
            if not existing:
                new_product = Product(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    price=product.price,
                    description=product.description,
                    tags=product.tags
                )
                postgres_session.add(new_product)
        postgres_session.commit()
        print(f"✓ Migrated {len(products)} products")
        
        # Migrate Interactions
        print("Migrating interactions...")
        interactions = sqlite_session.query(Interaction).all()
        for interaction in interactions:
            existing = postgres_session.query(Interaction).filter(Interaction.id == interaction.id).first()
            if not existing:
                new_interaction = Interaction(
                    id=interaction.id,
                    user_id=interaction.user_id,
                    product_id=interaction.product_id,
                    action_type=interaction.action_type
                )
                postgres_session.add(new_interaction)
        postgres_session.commit()
        print(f"✓ Migrated {len(interactions)} interactions")
        
        print("\n" + "="*50)
        print("✅ MIGRATION COMPLETE!")
        print("="*50)
        print(f"Total migrated:")
        print(f"  - {len(users)} users")
        print(f"  - {len(products)} products")
        print(f"  - {len(interactions)} interactions")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        postgres_session.rollback()
        raise
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    print("="*50)
    print("SQLite → PostgreSQL Migration")
    print("="*50)
    migrate_data()
