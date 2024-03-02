from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import proxy


urlpatterns = [
    path("", views.main_page, name="display_main_page"),
    path('login/', auth_views.LoginView.as_view(next_page='/'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_request, name="register"),
    path('add_parcel/', views.add_parcel, name="add_parcel"),
    path('archive/', views.archive, name="archive"),
    path('archive_parcel/<int:parcel_id>/', views.archive_parcel, name='archive_parcel'),
    path('unarchive_parcel/<int:parcel_id>/', views.unarchive_parcel, name='unarchive_parcel'),
    path('delete_parcel/<int:parcel_id>/', views.delete_parcel, name='delete_parcel'),
    path('proxy/<str:track_code>/', proxy, name='proxy'),
    path('accept_order/<int:parcel_id>/', views.accept_order, name='accept_order'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)