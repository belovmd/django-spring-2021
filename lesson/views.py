from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.http import HttpResponse

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


@login_required
def material_details(request, y, m, d, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 publish__year=y,
                                 publish__month=m,
                                 publish__day=d)
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.material = material
            new_comment.save()
            return redirect(material)
    else:
        comment_form = forms.CommentForm()

    return render(request,
                  'materials/detail.html',
                  {'material': material,
                   'form': comment_form,
                   })


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


def create_material(request):
    if request.method == "POST":
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()
            return render(request, 'materials/detail.html',
                          {'material': new_material})
    else:
        material_form = forms.MaterialForm()

    return render(request,
                  'materials/create.html',
                  {'form': material_form})


def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['login'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Logged in')
                else:
                    return HttpResponse('not active')
            else:
                return HttpResponse('bad credentials')
    else:
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})
