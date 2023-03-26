import re


def validate_email_address(email_address):
    """
    Used to validate email address
    :param email_address:
    :return:
    """
    if not re.search(
        r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address
    ):
        print(f"The email address {email_address} is not valid")
        return False
    return True
