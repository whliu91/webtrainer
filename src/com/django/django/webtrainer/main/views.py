from django.shortcuts import render
import json
from users.models import User

def login(request):
	return render(request, 'login.html')

def accounts_profile(request):
	if request.method == 'POST':
		a = json.loads(request.body)
		print(a)
		b = User.objects.get(email=request.user.email)
		b.username = a['name']
		b.company = a['company']
		b.save()
	return render(request, 'accounts_profile.html')
