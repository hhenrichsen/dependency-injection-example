
from uuid import UUID

from db.models.user import User


class Comment:
    def __init__(self, id: str, content: str, created: str, author: User, post_id: str):
        self.__uuid = UUID(id)
        self.__content = content
        self.__created = created
        self.__author = author
        self.__post_id = post_id

    def get_id(self) -> UUID:
        return self.__uuid

    def get_content(self) -> str:
        return self.__content

    def get_author(self) -> User:
        return self.__author

    def get_post_id(self) -> UUID:
        return self.__post_id
    
    def get_created(self) -> str:
        return self.__created
    
    def to_dict(self, public: bool) -> dict:
        return {
            'id': self.get_id(),
            'post_id': self.get_post_id(),
            'content': self.get_content(),
            'created': self.get_created(),
            'author': self.get_author().to_dict(public),
        }

    def __repr__(self) -> str:
        return f"@{self.get_author().get_username()}: {self.get_content()}"
