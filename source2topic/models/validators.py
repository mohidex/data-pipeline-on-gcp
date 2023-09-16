# Custom exception for validation errors
class ValidationError(Exception):
    pass

# Validators for the Product model
def validate_positive_price(value):
    if value <= 0:
        raise ValidationError("Price must be a positive number.")

def validate_non_empty_string(value):
    if not value.strip():
        raise ValidationError("String value cannot be empty or contain only whitespace.")
