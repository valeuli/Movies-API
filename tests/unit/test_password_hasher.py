from app.utils.password_hasher import BcryptPasswordHasher


class TestBcryptPasswordHasher:
    """
    Tests for BcryptPasswordHasher class.
    """

    def test_hash_password_returns_hashed_value(self):
        """
        Test that hash_password returns a hashed string.
        """
        password = "my_secure_password"
        hashed_password = BcryptPasswordHasher.hash_password(password)

        assert hashed_password != password
        assert isinstance(hashed_password, str)
        assert len(hashed_password) > 0

    def test_verify_password_success(self):
        """
        Test to verify that it returns True for a valid password and hash.
        """
        password = "my_secure_password"
        hashed_password = BcryptPasswordHasher.hash_password(password)

        assert BcryptPasswordHasher.verify_password(password, hashed_password) is True

    def test_verify_password_failure(self):
        """
        Test to verify that it returns False for an invalid password.
        """
        password = "my_secure_password"
        wrong_password = "wrong_password"
        hashed_password = BcryptPasswordHasher.hash_password(password)

        assert (
            BcryptPasswordHasher.verify_password(wrong_password, hashed_password)
            is False
        )

    def test_hash_password_is_unique(self):
        """
        Test to verify that a unique hash is generated for the same input.
        """
        password = "my_secure_password"
        hash1 = BcryptPasswordHasher.hash_password(password)
        hash2 = BcryptPasswordHasher.hash_password(password)

        assert hash1 != hash2
