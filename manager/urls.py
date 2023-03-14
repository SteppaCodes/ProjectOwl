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

    path('create-project/', createproject, name='create-project'),
    path('create-milestone/<str:id>', createmilestone, name='create-milestone'),

    path('project/<str:id>', ProjectPage, name='project-page'),

    path('update-project/<str:id>', updateproject,name='update-project'),
    path('update-milestone/<str:id>', updatemilestone,name='update-milestone'),

    path('delete-project/<str:id>', deleteproject, name='delete-project'),
    path('delete-milestone/<str:id>', deletemilestone, name='delete-milestone'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)