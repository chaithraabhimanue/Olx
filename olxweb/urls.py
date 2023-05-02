from django.urls import path
from olxweb import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns= [
    path("signup",views.Signupview.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("home",views.homeview.as_view(),name="home"),
    path("signout",views.Signoutview.as_view(),name="signout"),
    path("profile/add",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile/details",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:id>/change",views.ProfileUpdateView.as_view(),name="profile-update"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)