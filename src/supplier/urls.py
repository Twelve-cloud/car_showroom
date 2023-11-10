"""
urls.py: File, containing routes for a supplier application.
"""


from rest_framework.routers import SimpleRouter
from supplier import views


app_name: str = 'supplier'

router: SimpleRouter = SimpleRouter()

router.register(prefix='suppliers', viewset=views.SupplierViewSet, basename='supplier')

urlpatterns: list = router.urls
