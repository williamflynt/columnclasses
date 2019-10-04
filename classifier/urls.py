from django.urls import path

from classifier import views

app_name = "classifier"

urlpatterns = [
    path("", views.ClassifyView.as_view(), name="classify"),
    path("load-subs/", views.LoadSubsView.as_view(), name="load-subs"),
    path("upload/", views.SourceUploadView.as_view(), name="upload-files"),
]
