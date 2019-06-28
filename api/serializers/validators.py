from rest_framework.serializers import ValidationError


class Choices(object):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, value):
        governate = value.split(",")[-2]
        if governate not in self.choices:
            raise ValidationError(
                {"message": f"must be in {self.choices}"}
            )
