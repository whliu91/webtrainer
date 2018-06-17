from django.shortcuts import render
import json
from users.models import User

def index(request):
	return render(request, 'basemain.html')

def accounts_profile(request):
	print("[DEBUG] request on accounts_profile")
	if request.method == 'POST':
		print("[DEBUG] POST: user profile setting changed")
		profile_json = json.loads(request.body)
		user_profile_toChange = User.objects.get(email=request.user.email)
		user_profile_toChange.username = profile_json['name']
		user_profile_toChange.company = profile_json['company']
		user_profile_toChange.save()
	return render(request, 'accounts_profile.html')
