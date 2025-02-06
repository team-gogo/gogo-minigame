from django.contrib import admin
from django.urls import path, include
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()


urlpatterns = [
    path("admin/", admin.site.urls),
    path('minigame/', api.urls)
]
