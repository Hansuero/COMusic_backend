from django.shortcuts import render
from django.http import JsonResponse
from music.models import Song

from user.models import User
from comment.models import Comment


# Create your views here.
# 创建评论
def create_comment(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        song_id = request.POST.get('song_id')
        content = request.POST.get('content')
        song = Song.objects.get(id=song_id)
        Comment.objects.create(user=user, song=song, content=content)
        result = {'result': 0, 'message': r'发表评论成功！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


# 删除评论
def delete_comment(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'DELETE':
        username = request.session['username']
        comment_id = request.GET.get('comment_id')
        user = User.objects.get(username=username)
        # 找不到评论
        if not Comment.objects.filter(id=comment_id).exists():
            result = {'result': 3, 'message': r'未找到该评论'}
            return JsonResponse(result)
        comment = Comment.objects.get(id=comment_id)
        # 删除者不是创建评论者
        if user.id != comment.user.id:
            result = {'result': 4, 'message': r'您没有该权限!'}
            return JsonResponse(result)
        # 条件满足，从数据库将该评论删除
        comment.delete()
        result = {'result': 0, 'message': r'删除评论成功！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


# 修改评论
def change_comment(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'POST':
        username = request.session['username']
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')
        user = User.objects.get(username=username)
        # 找不到评论
        if not Comment.objects.filter(id=comment_id).exists():
            result = {'result': 3, 'message': r'未找到该评论'}
            return JsonResponse(result)
        comment = Comment.objects.get(id=comment_id)
        # 修改者不是创建评论者
        if user.id != comment.user.id:
            result = {'result': 4, 'message': r'您没有该权限!'}
            return JsonResponse(result)
        # 条件满足，更新评论内容并保存
        comment.content = content
        comment.save()
        result = {'result': 0, 'message': r'修改评论成功！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_comment(request):
    if request.method == 'GET':
        song_id = request.GET.get('song_id')
        comments = Comment.objects.filter(song__id=song_id)
        comments_data = [c.to_dic() for c in comments]
        result = {'result': 0, 'message': r'获取评论列表成功！', 'song_comments': comments_data}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)
