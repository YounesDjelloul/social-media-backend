from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', GetProfileDataView.as_view(), name='getprofiledata'),
    path('profile/update/', UpdateProfileDataView.as_view(), name='updateprofiledata'),
]