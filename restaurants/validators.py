from django.core.exceptions import ValidationError

def validate_real_domain(value):
    allowed_domains = ['gmail.com', 'abv.bg', 'yahoo.com', 'outlook.com', 'hypserve.com', 'mail.bg']

    domain = value.split('@')[-1].lower()

    if domain not in allowed_domains:
        raise ValidationError(
            f'The domain "{domain}" is not supported or looks fake. Please use a valid email provider.')
