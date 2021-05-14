from django.shortcuts import render, get_object_or_404

from . import models
# Create your views here.


def all_materials(request):
    material_list = models.Material.objects.all()
    return render(request,
                  'materials/all_materials.html',
                  {'materials': material_list})


def material_details(request, y, m, d, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 publish__year=y,
                                 publish__month=m,
                                 publish__day=d)
    return render(request,
                  'materials/detail.html',
                  {'material': material})
