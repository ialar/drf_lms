from rest_framework.serializers import ValidationError

youtube = 'https://www.youtube.com/'


def validate_not_youtube(link):
    if youtube not in link:
        raise ValidationError('Недопустимая ссылка, попробуйте YouTube.')
