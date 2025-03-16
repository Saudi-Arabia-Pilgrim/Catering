
def validate_gmail(gmail: str) -> bool:
    """
    Validate email
    :param gmail:
    :return: Boolean
    """
    return gmail.endswith('@gmail.com')
