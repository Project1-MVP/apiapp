from rest_framework import serializers
from .models import Tenant, TenantUser

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'business_name', 'subdomain', 'created_at', 'is_active']

class TenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['id', 'username', 'email', 'tenant', 'is_tenant_owner', 'role']
        extra_kwargs = {'password': {'write_only': True}}
