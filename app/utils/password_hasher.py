import bcrypt


class BcryptPasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Returns the hash for the password passed as a parameter using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Returns True if the password matches the hashed password.
        """
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
