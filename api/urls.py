from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"book", views.BookViewSet)
router.register(r"bookinstance", views.BookInstanceViewSet)
router.register(r"author", views.AuthorViewSet)


urlpatterns = router.urls
