import asyncio
import os
import sys
import subprocess
from sqlalchemy import text

# Add parent directory (project root) to sys.path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import engine
from app.core.config import settings

async def run_sql_file(file_path: str):
    """Executes a raw SQL file using SQLAlchemy."""
    base_dir = os.path.dirname(__file__)
    # Path relative to project root
    full_path = os.path.abspath(os.path.join(base_dir, "..", file_path))
    
    if not os.path.exists(full_path):
        print(f"Warning: SQL file not found: {full_path}")
        return

    print(f"Executing SQL: {full_path}...")
    with open(full_path, "r", encoding="utf-8") as f:
        sql = f.read()

    async with engine.begin() as conn:
        for statement in sql.split(";"):
            if statement.strip():
                await conn.execute(text(statement))
    print(f"Finished SQL: {file_path}")

def run_alembic():
    """Runs alembic upgrade head from project root."""
    print("Running Alembic Migrations...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True, cwd=root_dir)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: Migration Error: {result.stderr}")
        return False
    return True

async def run_seeders():
    """Runs all python scripts in database/seeders/."""
    base_dir = os.path.dirname(__file__)
    seeder_dir = os.path.join(base_dir, "seeders")
    if not os.path.exists(seeder_dir):
        return

    print("Running Seeders...")
    import importlib.util

    for filename in os.listdir(seeder_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            file_path = os.path.join(seeder_dir, filename)
            module_name = f"database.seeders.{filename[:-3]}"
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "run"):
                print(f"   Executing seeder: {filename}")
                if asyncio.iscoroutinefunction(module.run):
                    await module.run()
                else:
                    module.run()
    print("Seeders Finished")

async def create_db():
    import aiomysql
    # Parse connection string
    connection_url = settings.DATABASE_URL.replace("mysql+aiomysql://", "")
    auth, rest = connection_url.split("@")
    user, password = auth.split(":")
    host_port, db_name = rest.split("/")
    host, port = host_port.split(":")
    
    print(f"Connecting to MySQL at {host}:{port} as {user}...")
    try:
        conn = await aiomysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )
        async with conn.cursor() as cur:
            await cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.close()
        print(f"Database '{db_name}' is ready.")
    except Exception as e:
        print(f"Error creating database: {e}")

async def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "up"

    await create_db()

    if command == "up":
        await run_sql_file("database/sql/schema.sql")
        if run_alembic():
            await run_sql_file("database/sql/data.sql")
    
    elif command == "seed":
        await run_seeders()
        
    elif command == "all":
        await run_sql_file("database/sql/schema.sql")
        if run_alembic():
            await run_sql_file("database/sql/data.sql")
            await run_seeders()
    
    else:
        print("Usage: python database/migrate.py [up|seed|all]")

if __name__ == "__main__":
    asyncio.run(main())
