
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from api.views import AccountViewSet, LoginView, PackageViewSet, LogoutView, OfferViewSet, PackageCustomListViewSet, ClientAcceptDeliveryViewSet

router = DefaultRouter()
router.register("accounts",AccountViewSet)
router.register("packages",PackageViewSet)
router.register("offers", OfferViewSet)
router.register("packagelist", PackageCustomListViewSet,basename="packagelist")
router.register("offerconfirm", ClientAcceptDeliveryViewSet,basename="offerconfirm")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api/login/',LoginView.as_view(),name="login"),
    path('api/logout/',LogoutView.as_view(),name="logout"),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

