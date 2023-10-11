from django.shortcuts import render


def index(request):
	return render(request, 'list_apps/index.html')