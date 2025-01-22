from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        subdomain = host.split('.')[0]
        request.tenant = Tenant.objects.filter(subdomain=subdomain).first()
        return self.get_response(request)
