from app.utils.password_hasher import BcryptPasswordHasher


class SetupHelper:
    """
    Helper class to simplify test setup and user creation.
    """

    @staticmethod
    def create_test_user(
        service,
        email: str,
        password: str,
        first_name: str = "Test",
        last_name: str = "User",
    ):
        """
        Create a test user if it does not already exist.
        """
        user_data = service.get_user_by_email(email)
        if not user_data:
            hashed_password = BcryptPasswordHasher.hash_password(password)
            user_data = service.create_object(
                {
                    "email": email,
                    "password": hashed_password,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )
        return user_data
