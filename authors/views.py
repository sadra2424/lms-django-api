from rest_framework import viewsets, filters
from .models import Author
from rest_framework.permissions import IsAuthenticated
from .serializers import AuthorSerializer
from borrowers.permissions import IsAdminUser

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']