from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from .models import Tenant, TenantUser
from .serializers import TenantSerializer, TenantUserSerializer
from .permissions import IsTenantOwner

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsTenantOwner()]

    @swagger_auto_schema(
        operation_description="Create new tenant",
        responses={201: TenantSerializer()}
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TenantUserViewSet(viewsets.ModelViewSet):
    serializer_class = TenantUserSerializer
    permission_classes = [IsAuthenticated, IsTenantOwner]

    def get_queryset(self):
        return TenantUser.objects.filter(tenant=self.request.user.tenant)