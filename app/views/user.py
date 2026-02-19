from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from app.serializer.user import UserSerializer
from app.models.user import User

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class AuthCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        return Response(UserSerializer(request.user).data)
    def patch(self,request):
        user = request.user
        sr_user = UserSerializer(user, data=request.data,partial=True)
        sr_user.is_valid(raise_exception=True)
        sr_user.save()
        return Response(sr_user.data, status=status.HTTP_200_OK)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)