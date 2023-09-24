from django.core.exceptions import ValidationError

from phonenumbers import is_valid_number, parse
from phonenumbers.phonenumberutil import NumberParseException


def validate_phone(value: str) -> None:
    """
    Validates a phone number.
    Raises a ValidationError if the phone number is invalid or cannot be recognized
    """

    try:
        parsed_number = parse(value)
        if not is_valid_number(parsed_number):
            raise ValidationError("Invalid phone number")
    except NumberParseException:
        raise ValidationError("Phone number recognition error")