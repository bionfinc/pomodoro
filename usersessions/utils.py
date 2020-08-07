from django.contrib.auth.models import User


def get_info(request):
    user = User.objects.get(username=request.user.username)
    search_query = request.GET.get('search')
    page_num = request.GET.get('page')
    return user, search_query, page_num
