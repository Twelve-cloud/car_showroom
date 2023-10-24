"""
urls.py: File, containing routes for a core application.
"""

from rest_framework.routers import SimpleRouter
from core import views


app_name: str = 'core'

router: SimpleRouter = SimpleRouter()

router.register(prefix='cars', viewset=views.CarViewSet, basename='car')

urlpatterns: list = router.urls
