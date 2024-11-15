from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        # toteuta loput tarkastukset tänne ja nosta virhe virhetilanteissa

        if len(username) < 3:  
            raise UserInputError("Invalid username: minimum of 3 a-z characters")
        
        for sign in username: 
            if sign not in "abcdefghijklmnopqrstuvwxyz":
                raise UserInputError("Invalid username: only a-z characters")


        if len(password) < 8:                      
            raise UserInputError("Invalid password: minimum length 8")
        
        if password != password_confirmation:
            raise UserInputError("Invalid password: passwords do not match")

        for sign in password: 
            if sign not in "abcdefghijklmnopqrstuvwxyz":
                return
        raise UserInputError("Invalid password: not only characters")
        

user_service = UserService()
