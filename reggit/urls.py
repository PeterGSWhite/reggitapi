from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import PostViewSet, CreateVote, UserCreate, LoginView

router = DefaultRouter()
router.register('posts', PostViewSet, base_name='posts')


urlpatterns = [
    path("posts/<int:pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls
