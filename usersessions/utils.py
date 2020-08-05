from django.contrib.auth.models import User

def getInfo(request):
    user = User.objects.get(username=request.user.username)
    searchQuery = request.GET.get('search')
    page_num = request.GET.get('page')
    return user, searchQuery, page_num
