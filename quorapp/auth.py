from .models import UserProfile

def save_profile(strategy, details, response, user=None, *args, **kwargs):
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            attrs = dict(attrs.items())
            UserProfile.objects.create(
                **attrs
            )
