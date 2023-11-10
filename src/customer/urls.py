"""
urls.py: File, containing routes for a customer application.
"""


from rest_framework.routers import SimpleRouter
from customer import views


app_name: str = 'customer'

router: SimpleRouter = SimpleRouter()

router.register(prefix='customers', viewset=views.CustomerViewSet, basename='customer')

urlpatterns: list = router.urls
