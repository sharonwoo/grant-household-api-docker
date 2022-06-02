"""grants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

household_router = DefaultRouter()
household_router.register("", views.HouseholdViewSet, basename="API")

familymember_router = DefaultRouter()
familymember_router.register(
    "", views.FamilyMemberViewSet, basename="FamilyMemberAPI"
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/households/", include(household_router.urls)),
    path("api/v1/households/<int:id>/", include(household_router.urls)),
    path("api/v1/family_members/", include(familymember_router.urls)),
    path("api/v1/grants/", views.GrantList.as_view()),
    path("api/v2/grants-public/", views.GrantListPublic.as_view()),
]
