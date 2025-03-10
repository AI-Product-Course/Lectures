from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


password = "qwerty123!"
hashed_password = pwd_context.hash(password)
print(password)
print(hashed_password)
print(pwd_context.verify(password, hashed_password))
