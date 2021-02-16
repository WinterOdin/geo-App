from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  
from rest_framework.routers import DefaultRouter


from django.urls import path, include
from .views import LocationViewSet


router = DefaultRouter()
router.register('location', LocationViewSet, basename='Location')

urlpatterns = [

	path('', include(router.urls)),
	path('api-auth', include('rest_framework.urls')),
	path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
]
