import asyncio
from app.db.session import engine
from app.models.user import User
from app.core import security
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def debug_user():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == "muthu123@gmail.com"))
        user = result.scalars().first()
        
        if user:
            print(f"User found: {user.email}")
            print(f"Hashed password: {user.hashed_password}")
            
            # Verify with password123
            test_pw = "password123"
            match = security.verify_password(test_pw, user.hashed_password)
            print(f"Password 'password123' match: {match}")
            
            # Re-hash and update just in case
            if not match:
                print("Updating password to 'password123'...")
                user.hashed_password = security.get_password_hash(test_pw)
                await session.commit()
                print("Password updated!")
        else:
            print("User NOT found!")

if __name__ == "__main__":
    asyncio.run(debug_user())
