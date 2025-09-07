class Validators:

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False, 'Password length must be minimum 8.'
        return True, 'Valid password'