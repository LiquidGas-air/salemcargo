from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, ParcelForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect
from .models import Parcel, UserProfile
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt


def accept_order(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    parcel.status = 'DONE'  # or 'Принято клиентом'
    parcel.in_archive = True
    parcel.save()
    return redirect('/')  # replace with your redirect view


@xframe_options_exempt
def proxy(request, track_code):
    response = requests.get(f'https://t.17track.net/en?nums={track_code}', allow_redirects=False)
    # print(response.text)
    # if response.status_code == 301:
    #     # handle redirect here
    #     new_url = response.headers['Location']
    #     response = requests.get(new_url)
    return HttpResponse(response.content)

def delete_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    parcel.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def unarchive_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    parcel.in_archive = False
    parcel.save()
    return redirect('/archive')

def archive_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    parcel.in_archive = True
    parcel.save()
    return redirect('/')
    
def add_parcel(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.user = request.user
            parcel.status = 'CREATED'
            parcel.in_archive = False
            parcel.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = ParcelForm()
    return render(request, 'users/index.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def register_request(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1'),
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            phone_number = request.POST.get('phone_number')
            user_profile = UserProfile.objects.create(user=user, phone_number=phone_number)
            user_profile.save()

            return redirect('login')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request=request, template_name="registration/register.html", context={"register_form":NewUserForm})
    
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def main_page(request):
    parcels = request.user.parcels.exclude(in_archive=True)
    TRACKING_STATUSES = {
        'CREATED': 'Создано',
        'SHIPPED': 'Отправлено',
        'IN_TRANSIT': 'В пути',
        'DELIVERED': 'Доставлено',
        'RECEIVED': 'Получено клиентом',
        'DONE': 'Принято клиентом'
    }
    STATUSES = ['CREATED', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'RECEIVED', 'DONE']
    return render(request, 'users/index.html', {'parcels': parcels, 'statuses': STATUSES, 'dict_status': TRACKING_STATUSES})

@login_required
def archive(request):
    parcels = request.user.parcels.exclude(in_archive=False)
    TRACKING_STATUSES = {
        'CREATED': 'Создано',
        'SHIPPED': 'Отправлено',
        'IN_TRANSIT': 'В пути',
        'DELIVERED': 'Доставлено',
        'RECEIVED': 'Получено клиентом',
        'DONE': 'Принято клиентом'
    }
    STATUSES = ['CREATED', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'RECEIVED', 'DONE']
    return render(request, 'users/archive.html', {'parcels': parcels, 'statuses': STATUSES, 'dict_status': TRACKING_STATUSES})

