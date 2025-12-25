from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NavLinkViewSet, HeaderViewSet, HeroSlideViewSet, AboutViewSet,
    StatViewSet, DirectorViewSet, ContactInfoViewSet, FooterViewSet, PageViewSet, ImageBlockViewSet
)

router = DefaultRouter()
router.register(r'nav-links', NavLinkViewSet)
router.register(r'headers', HeaderViewSet)
router.register(r'hero-slides', HeroSlideViewSet)
router.register(r'about', AboutViewSet)
router.register(r'stats', StatViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'contact', ContactInfoViewSet)
router.register(r'footers', FooterViewSet)
router.register(r'pages', PageViewSet)
router.register(r'image-blocks', ImageBlockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

