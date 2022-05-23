from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Book
from utils.decorators import user_login_required


@api_view()
@user_login_required
def get_all_reviews(request):
    books = Book.objects.all().order_by('no')

    return Response({
        'success': True,
        'data': [
            {
                'id': book.no,
                'user_id': book.user.pk,
                'name': book.name,
                'title': book.title,
                'comment': book.comment
            }
            for book in books
        ]
    })


@api_view()
@user_login_required
def get_review(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except:
        return Response({'success': False, 'message': '查無資料'}, status=status.HTTP_404_NOT_FOUND)

    return Response({

        'success': True,
        'data': {
            'id': book.no,
            'user_id': book.user.pk,
            'name': book.name,
            'title': book.title,
            'comment': book.comment
        }
    })


@api_view()
@user_login_required
def get_critic_reviews(request):
    data = request.query_params
    user_id = data.get('user_id')

    user_id = str(user_id).strip()
    books = Book.objects.filter(user_id=user_id)

    return Response({
        'success': True,
        'data': [
            {
                'id': book.no,
                'user_id': book.user.pk,
                'name': book.name,
                'title': book.title,
                'comment': book.comment
            }
            for book in books
        ]
    })


@api_view(['POST'])
@user_login_required
def add_review(request):
    data = request.data
    try:
        Book.objects.create(user_id=data['user_id'], name=data['name'],
                            title=data['title'], comment=data['comment'])
        return Response({'success': True, 'message': '新增成功'})
    except:
        return Response({'success': False, 'message': '新增失敗'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@user_login_required
def edit_review(request, pk):
    data = request.data

    user_id = data.get('user_id')
    book = Book.objects.filter(no=pk, user_id=user_id)
    if not book.exists():
        return Response({'success': False, 'message': '沒有這本書'}, status=status.HTTP_404_NOT_FOUND)

    try:
        book.update(name=data['name'], title=data['title'], comment=data['comment'])
        return Response({'success': True, 'message': '編輯成功'})
    except:
        return Response({'success': False, 'message': '編輯失敗'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@user_login_required
def delete_review(request, pk):
    data = request.data

    user_id = data.get('user_id')
    book = Book.objects.filter(no=pk, user_id=user_id)
    if not book.exists():
        return Response({'success': False, 'message': '沒有這本書'}, status=status.HTTP_404_NOT_FOUND)

    book.delete()
    return Response({'success': True, 'message': '刪除成功'})
