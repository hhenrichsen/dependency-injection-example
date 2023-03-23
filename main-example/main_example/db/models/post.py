from uuid import UUID
from . import User


class Post:
    def __init__(self, id: str, title: str, content: str, created: str, author: User):
        self.__uuid = UUID(id)
        self.__title = title
        self.__content = content
        self.__created = created
        self.__author = author

    def get_id(self) -> UUID:
        return self.__uuid

    def get_title(self) -> str:
        return self.__title

    def get_content(self) -> str:
        return self.__content

    def get_author(self) -> User:
        return self.__author
    
    def get_created(self) -> User:
        return self.__created

    def to_dict(self, public: bool) -> dict:
        return {
            'id': self.get_id(),
            'title': self.get_title(),
            'created': self.get_created(),
            'author': self.get_author().to_dict(public),
            'content': self.get_content()
        }

    def __repr__(self) -> str:
        return f"{self.get_title()} by @{self.get_author().get_username()}\n {self.get_content()}"
