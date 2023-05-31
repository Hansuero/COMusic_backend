from django.http import JsonResponse
from django.shortcuts import render
from super_admin.models import Report
from user.models import User


# Create your views here.

def get_report_list(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'GET':
        username = request.session['username']
        user = User.objects.get(username=username)
        report_list = Report.objects.filter(receiver=user)
        if report_list:
            report_list_data = [r.to_dic() for r in report_list]
            result = {'result': 0, 'message': r'返回消息列表成功！', 'report_list': report_list_data}
            return JsonResponse(result)
        else:
            result = {'result': 3, 'message': r'消息列表为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


