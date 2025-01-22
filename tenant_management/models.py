from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Tenant(models.Model):
    business_name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_tenants')
    is_active = models.BooleanField(default=True)

class TenantUser(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_tenant_owner = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default='user')
