from django.urls import path
from django.views import View
from todo_app.views import HomeView

urlpatterns = [
        path('', HomeView.as_View(), name='home'),
        ]