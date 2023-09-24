from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Office, Team
from cars.models import Car


def home(request):
    staff = Team.objects.all()[:5]
    featured_cars = Car.objects.order_by('-created_at').filter(is_featured=True)
    latest_cars = Car.objects.order_by('-created_at')[:5]

    # Get all unique brands
    # search_fields = Car.objects.values('model').distinct()
    car_brands = Car.objects.values_list('brand', flat=True).distinct()
    car_models = Car.objects.values_list('model', flat=True).distinct()
    car_years = Car.objects.values_list('year', flat=True).distinct()

    offices = Office.objects.all()
    addresses = [office.get_address() for office in offices]
    locations = set(addresses)

    # print(locations)

    # engine_attribute = CarAttribute.objects.filter(name__iexact="engine").first()
    # engine_values = CarAttributeValue.objects.filter(
    #     attribute=engine_attribute
    # ).values_list('value', flat=True).distinct().order_by('value')

    # # Get all unique engines
    # engine_attribute = CarAttribute.objects.filter(name__iexact="engine").first()
    # engine_values = CarAttributeValue.objects.filter(
    #     attribute=engine_attribute
    # ).values_list('value', flat=True).distinct().order_by('value')

    data = {
        'staff': staff,
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'brands': car_brands,
        'models': car_models,
        'years': car_years,
        'locations': locations
    }
    return render(request, 'pages/home.html', data)


def about(request):
    return render(request, 'pages/about.html', context={"team": Team.objects.all()})


def services(request):
    return render(request, 'pages/services.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone'] if not None else "Not specified"
        message = request.POST['message']

        email_subject = f"Contact form: {subject} — {email}"
        email_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

        admins = get_user_model().objects.filter(is_superuser=True)
        send_mail(email_subject,
                  email_body,
                  "carzone@customers.com", [admin.email for admin in admins], fail_silently=False)
        messages.success(request, message="Thank you for contacting us. We will get back to you shortly")
        return redirect('contact')
    return render(request, 'pages/contact.html')
