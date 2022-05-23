from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Account
from utils.decorators import user_login_required


@api_view(['POST'])
def login(request):
    if 'user_id' in request.session:
        return Response({'success': False, 'message': '您已經登入'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    try:
        user = Account.objects.get(pk=data['id'], pwd=data['pwd'])
        request.session['user_id'] = user.id
        request.session.save()
        return Response({'success': True, 'message': '登入成功', 'sessionid':request.session.session_key})
    except Account.DoesNotExist:
        return Response({'success': False, 'message': '帳號或密碼錯誤'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@user_login_required
def logout(request):
    request.session.flush()
    return Response({'success': True, 'message': '登出成功'})