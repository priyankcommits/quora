from .models import Notification

def notification_create(question,type,notification_to,user_id):
    notification = Notification.objects.create(
            post_id = question,
            type = type,
            notification_id = notification_to,
            user_id = user_id
            )
    return 0


