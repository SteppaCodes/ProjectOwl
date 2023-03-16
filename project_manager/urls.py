from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-project/', createproject, name='create-project'),
    path('create-milestone/<str:id>', createmilestone, name='create-milestone'),
    path('create-task/<str:id>', createtask, name='create-task'),

    path('project/<str:id>', ProjectPage, name='project-page'),
    path('milestone/<str:id>', milestonepage, name='milestone-page'),

    path('start-task/<str:id>', starttask, name='start-task'),
    path('pause-task/<str:id>', pausetask, name='pause-task'),
    path('completed-task/<str:id>', pausetask, name='completed-task'),

    path('update-project/<str:id>', updateproject,name='update-project'),
    path('update-milestone/<str:id>', updatemilestone,name='update-milestone'),
    path('update-task/<str:id>', updatetask,name='update-task'),

    path('delete-project/<str:id>', deleteproject, name='delete-project'),
    path('delete-milestone/<str:id>', deletemilestone, name='delete-milestone'),
    path('delete-task/<str:id>', deletetask, name='delete-task'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

