"""
Database initialization and migration scripts for TruthLens AI
"""

import asyncio
import asyncpg
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection and migration manager"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def initialize_pool(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close_pool(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    async def execute_script(self, script_path: str) -> None:
        """Execute SQL script from file"""
        try:
            script_content = Path(script_path).read_text()
            
            async with self.pool.acquire() as conn:
                await conn.execute(script_content)
                logger.info(f"Successfully executed script: {script_path}")
                
        except Exception as e:
            logger.error(f"Failed to execute script {script_path}: {e}")
            raise
    
    async def run_migrations(self, migrations_dir: str = "database/migrations") -> None:
        """Run all migration scripts in order"""
        migrations_path = Path(migrations_dir)
        
        if not migrations_path.exists():
            logger.info(f"Migration directory {migrations_dir} does not exist")
            return
        
        migration_files = sorted(
            [f for f in migrations_path.glob("*.sql") if f.is_file()],
            key=lambda x: x.name
        )
        
        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file.name}")
            await self.execute_script(str(migration_file))
    
    async def check_connection(self) -> bool:
        """Test database connection"""
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def get_table_info(self, table_name: str) -> dict:
        """Get information about a specific table"""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow("""
                    SELECT 
                        schemaname,
                        tablename,
                        tableowner
                    FROM pg_tables 
                    WHERE tablename = $1
                """, table_name)
                
                if result:
                    # Get column information
                    columns = await conn.fetch("""
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable,
                            column_default
                        FROM information_schema.columns 
                        WHERE table_name = $1
                        ORDER BY ordinal_position
                    """, table_name)
                    
                    return {
                        "table_info": dict(result),
                        "columns": [dict(col) for col in columns]
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Failed to get table info for {table_name}: {e}")
            return None
    
    async def create_indexes(self) -> None:
        """Create performance indexes"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS CONCURRENTLY idx_articles_user_created ON articles(user_id, created_at DESC);",
            "CREATE INDEX IF NOT EXISTS CONCURRENTLY idx_articles_credibility ON articles(credibility_score);",
            "CREATE INDEX IF NOT EXISTS CONCURRENTLY idx_sources_domain_reliability ON sources(domain_name, reliability_score);",
            "CREATE INDEX IF NOT EXISTS CONCURRENTLY idx_cache_hash_expires ON analysis_cache(content_hash, expires_at);"
        ]
        
        async with self.pool.acquire() as conn:
            for index_sql in indexes:
                try:
                    await conn.execute(index_sql)
                    logger.info(f"Created index: {index_sql[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation failed: {e}")
    
    async def seed_data(self) -> None:
        """Seed initial data"""
        seed_data = [
            # Additional reliable sources
            ("npr.org", 94.1, "center-left", "high", "US", "news", "National Public Radio"),
            ("pbs.org", 92.8, "center", "high", "US", "news", "Public Broadcasting Service"),
            ("economist.com", 90.5, "center-right", "high", "UK", "news", "The Economist magazine"),
            ("time.com", 87.3, "center-left", "medium", "US", "news", "Time magazine"),
            
            # Additional unreliable sources
            ("breitbart.com", 35.7, "far-right", "low", "US", "news", "Breitbart News Network"),
            ("infowars.com", 12.4, "far-right", "very-low", "US", "conspiracy", "InfoWars conspiracy site"),
            ("naturalnews.com", 28.9, "far-right", "low", "US", "conspiracy", "Natural News conspiracy site"),
            ("beforeitsnews.com", 22.1, "conspiracy", "very-low", "US", "conspiracy", "Before It's News conspiracy site"),
        ]
        
        async with self.pool.acquire() as conn:
            for domain, reliability, bias, factual, country, category, notes in seed_data:
                try:
                    await conn.execute("""
                        INSERT INTO sources (domain_name, reliability_score, bias_rating, factual_reporting, country, category, notes)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        ON CONFLICT (domain_name) DO NOTHING
                    """, domain, reliability, bias, factual, country, category, notes)
                    logger.info(f"Seeded source: {domain}")
                except Exception as e:
                    logger.warning(f"Failed to seed source {domain}: {e}")


async def main():
    """Main database initialization function"""
    import os
    from app.config import settings
    
    # Initialize database manager
    db_manager = DatabaseManager(settings.database_url)
    
    try:
        await db_manager.initialize_pool()
        
        # Test connection
        if not await db_manager.check_connection():
            raise Exception("Database connection failed")
        
        # Run main schema
        await db_manager.execute_script("database/init.sql")
        
        # Create additional indexes
        await db_manager.create_indexes()
        
        # Seed initial data
        await db_manager.seed_data()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        await db_manager.close_pool()


if __name__ == "__main__":
    asyncio.run(main())
