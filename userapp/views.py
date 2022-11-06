from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json

from userapp.models import User

# Create your views here.
class UserPersonalityCreateView(View):
    def post(self, request):
        if(request.user.is_anonymous):
            return JsonResponse({"message": "Unauthorized"})
        data = json.loads(self.request.body)
        user = get_object_or_404(User, id=request.user.id)
        user.person_type = data["person_type"]
        user.select_view = data["preference"]["view"]
        user.select_cafe = data["preference"]["cafe"]
        user.select_drink = data["preference"]["drink"]
        user.select_activity = data["preference"]["activity"]
        user.select_food = data["preference"]["food"]
        user.save()
        return JsonResponse({"message": "success"})