from django.shortcuts import render


def index(request):
	list_apps = ['http://127.0.0.1:8000/blog/']
	return render(request, 'list_apps/index.html', {'list_apps': list_apps})