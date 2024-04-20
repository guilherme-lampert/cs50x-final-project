import re

def check_password(password):
    """Check if user password is valid"""

    regex = "^(?=.*?[0-9])(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z0-9_]).{8,}$"

    if re.search(regex, password):
        return True

    return False