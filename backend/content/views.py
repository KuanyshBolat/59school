from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import (
    NavLink, Header, HeroSlide, About, Stat, Director, ContactInfo, Footer, Page, ImageBlock
)
from .serializers import (
    NavLinkSerializer, HeaderSerializer, HeroSlideSerializer, AboutSerializer,
    StatSerializer, DirectorSerializer, ContactInfoSerializer, FooterSerializer,
    PageSerializer, ImageBlockSerializer
)

class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

class NavLinkViewSet(ReadOnlyViewSet):
    queryset = NavLink.objects.all()
    serializer_class = NavLinkSerializer

class HeaderViewSet(ReadOnlyViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer

class HeroSlideViewSet(ReadOnlyViewSet):
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer

class AboutViewSet(ReadOnlyViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class StatViewSet(ReadOnlyViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

class DirectorViewSet(ReadOnlyViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class ContactInfoViewSet(ReadOnlyViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

class FooterViewSet(ReadOnlyViewSet):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer

class PageViewSet(ReadOnlyViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class ImageBlockViewSet(ReadOnlyViewSet):
    queryset = ImageBlock.objects.all()
    serializer_class = ImageBlockSerializer

