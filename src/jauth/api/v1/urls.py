"""
urls.py: File, containing routes for a jauth application.
"""


from rest_framework.routers import SimpleRouter
from jauth.api.v1 import views


app_name: str = 'jauth'

router: SimpleRouter = SimpleRouter()

router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='token', viewset=views.TokenViewSet, basename='token')

urlpatterns: list = router.urls
