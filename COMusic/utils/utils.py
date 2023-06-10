from super_admin.models import Report
from user.models import User


def create_report(sender, receiver, content):
    Report.objects.create(sender=sender, receiver=receiver, content=content)


def get_admin():
    return User.objects.get(username='admin')


def song_to_tomcat_url(song_id):
    result = 'http://82.157.165.72:8888/song/' + song_id + '_song.mp3'
    return result


def song_cover_to_tomcat_url(song_id, ext):
    result = 'http://82.157.165.72:8888/song_cover/' + song_id + '_song_cover.' + ext
    return result


def photo_to_tomcat_url(user_id, ext):
    result = 'http://82.157.165.72:8888/photo/' + user_id + '_photo.' + ext
    return result