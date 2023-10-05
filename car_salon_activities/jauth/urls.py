"""
urls.py: File, containing routes for an jauth application.
"""


from rest_framework.routers import SimpleRouter
from jauth import views


app_name: str = 'jauth'

router: SimpleRouter = SimpleRouter()

router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns: list = router.urls
