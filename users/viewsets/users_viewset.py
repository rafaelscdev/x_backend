from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Users
from users.serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Users.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        user = request.user

        if request.method == "GET":
            serializer = UsersSerializer(user, context={"request": request})
            return Response(serializer.data)

        elif request.method == "PATCH":
            serializer = UsersSerializer(
                user, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
