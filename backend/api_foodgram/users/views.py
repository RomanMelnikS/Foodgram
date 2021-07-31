# from rest_framework import filters, viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import CustomUser
# from .serializers import UsersSerializer


# class UsersViewSet(viewsets.ModelViewSet):
#     serializer_class = UsersSerializer
#     permission_classes = (IsAuthenticated)
#     filter_backends = (filters.SearchFilter, filters.OrderingFilter)
#     lookup_field = 'username'
#     queryset = CustomUser.objects.all()
#     search_fields = ('user__username',)
#     ordering = ('username',)
