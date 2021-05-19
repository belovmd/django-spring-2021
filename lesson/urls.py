from django.urls import path

from . import views

app_name = 'lesson'

urlpatterns = [
    path('', views.all_materials, name='all_materials'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>', views.material_details,
         name='material_details'),
    path('<int:material_id>/share/', views.share_material,
         name='share_material'),
    path('create/', views.create_material, name='create_material'),
]
