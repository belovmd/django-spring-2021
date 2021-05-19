from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from . import forms
from . import models


BODY_TEMPLATE = (
    '{title} at {uri} was recommended to you by {name}.\n\n'
    'Comment: {comment}'
)


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


def _prepare_mail(material, cd, request):

    uri = request.build_absolute_uri(material.get_absolute_url())
    body = BODY_TEMPLATE.format(
        title=material.title,
        uri=uri,
        name=cd['my_name'],
        comment=cd['comment'],
    )
    subject = "{name} recommends you {title}".format(
        name=cd['my_name'],
        title=material.title,
    )
    return subject, body


def share_material(request, material_id):
    material = get_object_or_404(models.Material,
                                 id=material_id)

    sent = False
    if request.method == "POST":
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject, body = _prepare_mail(material, cd, request)
            send_mail(subject, body, 'admin@supersite.com', (cd['to_email'], ))
            sent = True
    else:
        form = forms.EmailMaterialForm()

    return render(request,
                  'materials/share.html',
                  {'form': form,
                   'material': material,
                   'sent': sent})
