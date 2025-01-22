from rest_framework import permissions

class IsTenantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_tenant_owner

class HasAPIAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.tenant == request.tenant
