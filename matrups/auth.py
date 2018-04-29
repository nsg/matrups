# pylint: disable=missing-docstring

class Auth:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_verification_code(self):
        # pylint: disable=no-self-use
        """ This is supposed to return the OTP token. Because I'm
            not using OTP on my bot account I have left this
            unimplemented.
        """
        return None
