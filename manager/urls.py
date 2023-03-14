from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('signup', signup,name='signup'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('switch-account/', switchaccount,name='switch-account'),

    path('join-company',joincompany, name='join-company'),

    path('company/<str:id>', companypage, name='company-page'),
    path('user-dashboard/<str:id>',userdashboard ,name='user-dashboard'),

    path('project/<str:id>', ProjectPage, name='project-page'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)