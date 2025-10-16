"""
Database models and initialization using SQLAlchemy ORM
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Handle SQLite vs PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
elif DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Default to SQLite for local development
    engine = create_engine(
        "sqlite:///./ecommerce.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    interactions = relationship("Interaction", back_populates="user")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    tags = Column(String)  # Comma-separated tags
    
    interactions = relationship("Interaction", back_populates="product")


class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    action_type = Column(String, nullable=False)  # 'view', 'click', 'purchase'
    
    user = relationship("User", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")


def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def seed_mock_data():
    """Seed the database with mock data"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(User).count() > 0:
        print("Database already contains data. Skipping seed.")
        db.close()
        return
    
    # Create users
    users = [
        User(id=1, name="Alice Johnson"),
        User(id=2, name="Bob Smith"),
        User(id=3, name="Charlie Brown"),
        User(id=4, name="Diana Prince"),
    ]
    db.add_all(users)
    
    # Create products
    products = [
        Product(id=1, name="Wireless Mouse", category="Electronics", price=29.99, 
                description="Ergonomic wireless mouse with long battery life", 
                tags="electronics,computer,wireless,accessories"),
        Product(id=2, name="Mechanical Keyboard", category="Electronics", price=89.99,
                description="RGB mechanical gaming keyboard", 
                tags="electronics,computer,gaming,keyboard"),
        Product(id=3, name="USB-C Hub", category="Electronics", price=45.99,
                description="7-in-1 USB-C hub with HDMI and card reader", 
                tags="electronics,computer,accessories,usb"),
        Product(id=4, name="Laptop Stand", category="Accessories", price=35.99,
                description="Adjustable aluminum laptop stand", 
                tags="accessories,laptop,desk,ergonomic"),
        Product(id=5, name="Bluetooth Speaker", category="Electronics", price=59.99,
                description="Portable waterproof Bluetooth speaker", 
                tags="electronics,audio,bluetooth,portable"),
        Product(id=6, name="Noise Cancelling Headphones", category="Electronics", price=199.99,
                description="Premium over-ear headphones with active noise cancellation", 
                tags="electronics,audio,headphones,noise-cancelling"),
        Product(id=7, name="Webcam 1080p", category="Electronics", price=79.99,
                description="Full HD webcam with auto-focus", 
                tags="electronics,camera,video,streaming"),
        Product(id=8, name="Phone Stand", category="Accessories", price=15.99,
                description="Adjustable phone holder for desk", 
                tags="accessories,phone,desk,holder"),
        Product(id=9, name="LED Desk Lamp", category="Home", price=39.99,
                description="Dimmable LED desk lamp with USB charging port", 
                tags="home,lighting,desk,led"),
        Product(id=10, name="Wireless Charger", category="Electronics", price=24.99,
                description="Fast wireless charging pad for phones", 
                tags="electronics,charging,wireless,phone"),
        Product(id=11, name="Gaming Mouse Pad", category="Accessories", price=19.99,
                description="Large RGB gaming mouse pad", 
                tags="accessories,gaming,mouse,rgb"),
        Product(id=12, name="Portable SSD 1TB", category="Electronics", price=129.99,
                description="Ultra-fast portable solid state drive", 
                tags="electronics,storage,ssd,portable"),
        Product(id=13, name="Cable Management Kit", category="Accessories", price=12.99,
                description="Complete cable organizer set", 
                tags="accessories,cable,organization,desk"),
        Product(id=14, name="Monitor Arm", category="Accessories", price=69.99,
                description="Adjustable monitor mount arm", 
                tags="accessories,monitor,desk,ergonomic"),
        Product(id=15, name="Wireless Earbuds", category="Electronics", price=79.99,
                description="True wireless earbuds with charging case", 
                tags="electronics,audio,earbuds,wireless"),
    ]
    db.add_all(products)
    
    # Create interactions (user behavior)
    interactions = [
        # Alice - interested in audio products
        Interaction(user_id=1, product_id=5, action_type="view"),
        Interaction(user_id=1, product_id=6, action_type="view"),
        Interaction(user_id=1, product_id=5, action_type="purchase"),
        Interaction(user_id=1, product_id=15, action_type="view"),
        
        # Bob - computer accessories enthusiast
        Interaction(user_id=2, product_id=1, action_type="view"),
        Interaction(user_id=2, product_id=2, action_type="view"),
        Interaction(user_id=2, product_id=1, action_type="purchase"),
        Interaction(user_id=2, product_id=11, action_type="view"),
        Interaction(user_id=2, product_id=11, action_type="purchase"),
        Interaction(user_id=2, product_id=4, action_type="view"),
        
        # Charlie - setting up home office
        Interaction(user_id=3, product_id=4, action_type="view"),
        Interaction(user_id=3, product_id=9, action_type="view"),
        Interaction(user_id=3, product_id=9, action_type="purchase"),
        Interaction(user_id=3, product_id=14, action_type="view"),
        Interaction(user_id=3, product_id=7, action_type="view"),
        
        # Diana - mobile accessories
        Interaction(user_id=4, product_id=8, action_type="view"),
        Interaction(user_id=4, product_id=10, action_type="view"),
        Interaction(user_id=4, product_id=10, action_type="purchase"),
        Interaction(user_id=4, product_id=15, action_type="view"),
    ]
    db.add_all(interactions)
    
    # Commit all changes
    db.commit()
    print("✅ Database seeded successfully with mock data!")
    db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    seed_mock_data()
