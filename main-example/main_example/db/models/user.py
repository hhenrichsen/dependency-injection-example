from uuid import UUID

class User:
    def __init__(self, id: str, username: str, display_name: str, email: str):
        self.__uuid = UUID(id)
        self.__username = username
        self.__display_name = display_name
        self.__email = email
        
    def get_id(self) -> UUID:
        return self.__uuid
    
    def get_email(self) -> str:
        return self.__email
    
    def get_username(self) -> str:
        return self.__username
    
    def get_display_name(self) -> str:
        return self.__display_name
    
    def to_dict(self, public: bool = True) -> dict:
        value = {
            'id': self.get_id(),
            'username': self.get_username(),
            'displayName': self.get_display_name(),
            'email': self.get_email()
        }
        if public:
            del value['email']
        return value
    
    def __repr__(self) -> str:
        return f"@{self.get_username()} - {self.get_display_name()} ({self.get_email()}) ({self.get_id()})"