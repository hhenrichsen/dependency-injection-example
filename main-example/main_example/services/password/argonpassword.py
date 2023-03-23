from argon2 import PasswordHasher

from services.password import PasswordService

class Argon2PasswordService(PasswordService):
    def __init__(self):
        self.__hasher = PasswordHasher()
        
    def hash(self, raw: str) -> str:
        return self.__hasher.hash(raw)
        
    def valid(self, raw: str, hashed: str) -> bool:
        try:
            self.__hasher.verify(hashed, raw)
            return True
        except:
            return False