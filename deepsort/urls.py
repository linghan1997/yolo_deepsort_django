from django.urls import path
from .views import live, process_manager

urlpatterns = [
    path('stream/', live),
    path('run/<int:run>/', process_manager)  # run = 1: start tracking,  0: stop tracking
]