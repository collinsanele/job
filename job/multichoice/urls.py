from django.urls import path
from . import views

urlpatterns = [
	path('', views.landing),
    path('start/', views.start, name="start"),
	path('outcome/', views.outcome, name="outcome"),
	path('dashboard/', views.dashboard, name="dashboard"),
	path("before-create/", views.before_create, name="before_create"),
	path("create-story/", views.create_story, name="create_story"),
	path("create-question/", views.create_question, name="create_question"),
	path("edit-delete/", views.edit_delete, name="edit_delete"),
	path("edit/<int:pk>/", views.edit, name="edit"),
	path("delete/<int:pk>/", views.delete, name="delete"),
]