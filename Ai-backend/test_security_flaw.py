from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash_old(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    if len(password) > 72:
        password = password[:72]
    # This is what's in security.py right now
    return pwd_context.hash(password.decode('utf-8') if isinstance(password, bytes) else password)

def verify_password_old(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

password = "password123"
hashed = get_password_hash_old(password)
match = verify_password_old(password, hashed)

print(f"Password: {password}")
print(f"Hashed: {hashed}")
print(f"Match: {match}")

# Test if it fails with specific characters or if it's just flaky
for i in range(5):
    h = get_password_hash_old(password)
    m = verify_password_old(password, h)
    print(f"Attempt {i+1}: {m}")
