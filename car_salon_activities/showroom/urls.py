"""
urls.py: File, containing routes for a showroom application.
"""


from rest_framework.routers import SimpleRouter
from showroom import views


app_name: str = 'showroom'

router: SimpleRouter = SimpleRouter()

router.register(prefix='showrooms', viewset=views.ShowroomViewSet, basename='showroom')

urlpatterns: list = router.urls
