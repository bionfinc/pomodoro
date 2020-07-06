from django.shortcuts import render

# Create your views here.
def login_view(request, *args, **kwargs):
	my_context = {
	}

	return render(request, 'accounts/login.html', my_context)