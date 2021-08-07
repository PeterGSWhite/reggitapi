from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate


from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer, UserSerializer

class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"user_id": user.id})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny(), ]        
        return super(PostViewSet, self).get_permissions()

    def destroy(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if not request.user == post.created_by:
            raise PermissionDenied("You can not delete this post.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        if not request.user == post.created_by:
            raise PermissionDenied("You can not update this post.")
        return super().update(request, pk=pk)

    def partial_update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        if not request.user == post.created_by:
            raise PermissionDenied("You can not update this post.")
        return super().partial_update(request, pk=pk)


class CreateVote(APIView):
   def post(self, request, pk):
        value = request.data.get("value")
        data = {'post': pk, 'user': request.user.id, 'value': value}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteList(generics.ListAPIView):
    serializer_class = VoteSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Vote.objects.filter(user=user.id)