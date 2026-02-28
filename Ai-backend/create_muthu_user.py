import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.core import security
from sqlalchemy.future import select

async def create_muthu():
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Check if exists
        result = await session.execute(select(User).filter(User.email == "muthu123@gmail.com"))
        user = result.scalars().first()
        
        if not user:
            print("Creating user muthu123@gmail.com...")
            hashed = security.get_password_hash("password123")
            new_user = User(email="muthu123@gmail.com", hashed_password=hashed, name="Muthu")
            session.add(new_user)
            await session.commit()
            print("Successfully created!")
        else:
            print("User already exists!")

if __name__ == "__main__":
    asyncio.run(create_muthu())
