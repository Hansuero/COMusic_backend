from super_admin.models import Report
from user.models import User


def create_report(sender, receiver, content):
    Report.objects.create(sender=sender, receiver=receiver, content=content)


def get_admin():
    return User.objects.get(username='admin')
