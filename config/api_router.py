from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from medium.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("site_users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
