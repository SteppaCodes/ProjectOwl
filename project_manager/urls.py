from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #create
    path('create-project/', create_update_project, name='create-project'),
    path('create-milestone/<str:id>', create_update_milestone, name='create-milestone'),
    path('create-task/<str:id>', create_update_task, name='create-task'),
    path('milestone/<int:milestone_id>/addfile/',addfile, name='add_milestone_attachment'),
    path('project/<int:project_id>/addfile/',addfile, name='add_project_attachment'),
    path('task/<int:id>/New-Note/',create_update_note, name='create-note'),

    #Read
    path('project/<str:id>', ProjectPage, name='project-page'),
    path('milestone/<str:id>', milestonepage, name='milestone-page'),
    path('company-files/', files, name='files'),
    path('milestone/task/<str:id>/',taskpage, name='task-page'),
    path('files/<str:id>/',fileview, name='file-view'),

    #Update task
    path('milestone/<str:id>/update-task/<str:task_id>', create_update_task, name='update-task'),
    path('start-task/<str:id>', starttask, name='start-task'),
    path('pause-task/<str:id>', pausetask, name='pause-task'),
    path('completed-task/<str:id>', completetask, name='completed-task'),
    path('task/<int:id>/update-Note/<str:note_id>/',create_update_note, name='update-note'),

    #Update
    path('update-project/<str:project_id>', create_update_project,name='update-project'),
    path('project/<str:id>/update-milestone/<str:milestone_id>', create_update_milestone,name='update-milestone'),
    path('milestone/<str:id>/update-task/<str:task_id>', create_update_task,name='update-task'),
    path('update-file/<str:attachment_id>', addfile,name='update-file'),

    #Delete
    path('delete-project/<str:id>', deleteproject, name='delete-project'),
    path('delete-milestone/<str:id>', deletemilestone, name='delete-milestone'),
    path('delete-task/<str:id>', deletetask, name='delete-task'),
    path('delete-file/<str:id>', deletefile, name='delete-file'),
    path('delete-note/<str:id>', deletenote, name='delete-note'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

