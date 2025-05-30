# notes/urls.py
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'', NoteViewSet, basename='notes')
urlpatterns = router.urls