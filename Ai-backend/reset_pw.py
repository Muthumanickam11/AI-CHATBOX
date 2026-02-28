import asyncio
from app.db.session import engine
from app.models.user import User
from app.core import security
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def reset_password():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == "msdmuthu077@gmail.com"))
        user = result.scalars().first()
        
        if user:
            print(f"Resetting password for {user.email}...")
            user.hashed_password = security.get_password_hash("password123")
            await session.commit()
            print("Password reset to 'password123' successfully!")
        else:
            print("User not found!")

if __name__ == "__main__":
    asyncio.run(reset_password())
