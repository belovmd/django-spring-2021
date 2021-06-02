from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'lesson'


class MyHack(auth_views.PasswordResetView):
    success_url = reverse_lazy('lesson:password_reset_done')


urlpatterns = [
    # path('', views.all_materials, name='all_materials'),
    path('', views.MaterialListView.as_view(), name='all_materials'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>/', views.material_details,
         name='material_details'),
    path('<int:material_id>/share/', views.share_material,
         name='share_material'),
    path('create/', views.create_material, name='create_material'),
    # path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_reset/', MyHack.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('lesson:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.view_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)