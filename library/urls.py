from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.library_entries, name="entries"),
    path("entries/<int:id>/", views.library_entry_by_id, name="library_entry_by_id")
]