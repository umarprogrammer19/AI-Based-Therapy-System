#!/usr/bin/env python3
"""
Script to reset the database by dropping all tables and recreating them.
This addresses schema mismatch issues between the models and the existing database.
"""

import asyncio
from src.config.database import engine, drop_tables, create_tables


async def reset_database():
    """Reset the database by dropping and recreating all tables."""
    print("Dropping all tables...")
    await drop_tables()
    print("All tables dropped successfully.")

    print("Creating all tables...")
    await create_tables()
    print("All tables created successfully.")

    print("Database reset complete!")


if __name__ == "__main__":
    asyncio.run(reset_database())