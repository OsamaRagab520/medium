from django.urls import include, path

urlpatterns = [
    path("users/", include(("medium.users.urls", "users"))),
]
