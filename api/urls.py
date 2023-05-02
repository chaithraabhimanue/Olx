from rest_framework.urls import path
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

router=DefaultRouter()
router.register("accounts/users",views.Usercreation,basename="users"),
router.register("users/profile",views.ProfileView,basename="profile"),
router.register("v1/products",views.ProductsView,basename="products"),
router.register("questions",views.ChatBoxView,basename="questions"),
# router.register("answers",views.AnswersView,basename="answers")
urlpatterns = [
    path("token/",ObtainAuthToken.as_view())
    # path("token/",TokenObtainPairView.as_view()),
    # path("token/refresh/",TokenRefreshView.as_view())
]+router.urls
