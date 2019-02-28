from django.core.exceptions import ValidationError

def user_not_client(value):
    if not(User.objects.get(id=value).is_client):
        raise ValidationError("must be client")


