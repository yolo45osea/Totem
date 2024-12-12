from django.contrib.auth.backends import BaseBackend
from .models import Admin

class AdminBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(email=email)
            if admin.check_password(password):
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, admin_id):
        try:
            return Admin.objects.get(pk=admin_id)
        except Admin.DoesNotExist:
            return None
