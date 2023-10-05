"""
urls.py: File, containing routes for an auth application.
"""


from rest_framework.routers import SimpleRouter

from auth import views


app_name: str = 'auth'

router: SimpleRouter = SimpleRouter()

router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns: list = router.urls
