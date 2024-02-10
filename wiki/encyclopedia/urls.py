from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_content, name="content"),
    path("wiki", views.search_entry, name="search"),
    path("NewPage", views.create_new_page, name="new_page"),
    path("EditPage/<str:title>", views.edit_page, name="edit_page"),
    path("Random", views.random_page, name="random")
]
