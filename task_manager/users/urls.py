from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersListView.as_view(), name='user_list'),
    path('create/', views.SignUpView.as_view(), name='register'),
    path('<int:pk>/update/',
         views.UserUpdateView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/',
         views.UserDeleteView.as_view(),
         name='user_del'),
]
