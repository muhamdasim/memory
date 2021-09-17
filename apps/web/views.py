import jwt
import stripe

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from apps.web import repo
from apps.web.forms import PasswordChangeForm, ProfileChangeForm

@login_required
def home(request):
    patient_repo = repo.PatientRepo()
    patient_list = patient_repo.list(request.user)
    paginator = Paginator(patient_list, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'active_tab': 'home',
        'page_obj': page_obj,
    }
    return render(request, 'web/pages/home/home.html', context)

@login_required
def patient_list(request):
    patient_repo = repo.PatientRepo()
    patient_list = patient_repo.list(request.user)
    paginator = Paginator(patient_list, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'active_tab': 'patients',
        'page_obj': page_obj,
    }
    return render(request, 'web/pages/patients/patient_list.html', context)


@login_required
def therapy(request):
    repo_patient = repo.PatientRepo()
    context = {
        'active_tab': 'therapy',
        'patients': repo_patient.list(request.user)
    }
    if request.method == "POST":
        token = jwt.encode({'patient': request.POST['patient']}, "secret", algorithm="HS256")
        confirm_token = jwt.encode({'is_confirmed': 'no'}, "secret", algorithm="HS256")
        context["link"] = f"http://{request.META['HTTP_HOST']}/therapy/session/{token}/c/{confirm_token}"
        context["selected_patient"] = int(request.POST['patient'])

    return render(request, 'web/pages/therapy/index.html', context)


def therapy_client_site(request, token, c_token):
    repo_patient = repo.PatientRepo()

    data = jwt.decode(token, "secret", algorithms=["HS256"])
    confirmation = jwt.decode(c_token, "secret", algorithms=["HS256"])
    patient = repo_patient.get(data["patient"])
    if confirmation.get('is_confirmed', 'no') == 'no':
        context = {
            'patient': patient,
            'token': token,
            'c_token': c_token
        }
        return render(request, 'web/pages/therapy/client_confirm.html', context)
    context = {
        'patient': patient.id,
        "token": token
    }
    return render(request, 'web/pages/therapy/client.html', context)


def therapy_client_confirm(request, token, c_token):
    if request.method == "POST":
        confirmation = {'is_confirmed': 'yes'}
        confirm_token = jwt.encode(confirmation, "secret", algorithm="HS256")
        return redirect("web:therapy_client_site", token=token, c_token=confirm_token)


@login_required
def account_settings(request):
    context = dict()
    context['active_tab'] = 'account'

    if request.method == 'GET':
        # Password Change form
        context['passchange_form'] = PasswordChangeForm()

        # Profile Change form
        context['profilechange_form'] = ProfileChangeForm(data={
            'email': request.user.email,
            'username': request.user.username,
            'language': request.user.language,
            'is_subscribe': request.user.is_subscribe
        })

    elif request.method == 'POST':
        if 'passchange_form' in request.POST:
            form = PasswordChangeForm(request.POST)

            cur_pass = request.POST.get('cur_pass')
            cur_user = request.user
            if cur_user.check_password(cur_pass) is False:
                form.set_cur_pass_notmatch()
            if form.is_valid():
                cur_user.set_password(form.cleaned_data.get('new_pass'))
                messages.info(request, "Your password has been changed")
                cur_user.save()

            context['passchange_form'] = form

        elif 'profilechange_form' in request.POST:
            form = ProfileChangeForm(request.POST)
            if form.is_valid():
                cur_user = request.user
                cur_user.username = form.cleaned_data.get('username', cur_user.username)
                cur_user.save()
                messages.info(request, "Your profile has been updated")
            context['profilechange_form'] = form

    # User
    context['user'] = request.user
    context['subscription'] = request.user.active_stripe_subscription
    return render(request, 'web/pages/account_settings.html', context)


@login_required
def account_settings_delete(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect("/accounts/login/")


@login_required
def account_subscription(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    prices = stripe.Price.list()
    context = {
        "prices": prices.data
    }
    return render(request, 'web/pages/account/account_subscription.html', context=context)


@login_required
def account_subscription_success(request):
    return render(request, 'web/pages/account/account_subscribe_success.html')


@login_required
def account_subscription_canceled(request):
    return render(request, 'web/pages/account/account_subscribe_cancel.html')


def termsAndConditions(request):
    return render(request, 'web/pages/terms-and-conditions.html')


def contactUs(request):
    return render(request, 'web/pages/terms-and-conditions.html')


def faq(request):
    return render(request, 'web/pages/terms-and-conditions.html')