from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Users

from .serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_class = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('username',)

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_class=(permissions.IsAuthenticated,))
    def user_own_account(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
