from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Certificate
from .serializers import CertificateSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Certificate.objects.all()
        category = self.request.query_params.get('category', None)
        level = self.request.query_params.get('level', None)

        if category:
            queryset = queryset.filter(category=category)
        if level:
            queryset = queryset.filter(level=level)

        return queryset