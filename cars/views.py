from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from cars.models import Car
from pages.models import Office


def get_car_values():
    return {
        'brands': Car.objects.values_list('brand', flat=True).distinct(),
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'years': Car.objects.values_list('year', flat=True).distinct(),
    }

def get_office_locations():
    offices = Office.objects.all()
    addresses = [office.get_address() for office in offices]
    return set(addresses)


def cars(request):
    cars = Car.objects.order_by('-created_at')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

    car_values = get_car_values()
    locations = get_office_locations()

    data = {
        'cars': paged_cars,
        'locations': locations,
        **car_values
    }

    return render(request, 'cars/cars.html', data)


def car_detail(request, id):
    car = get_object_or_404(Car, pk=id)
    return render(request, 'cars/car_detail.html', {'car': car})


def search(request):
    cars = Car.objects.order_by('-created_at')
    car_values = get_car_values()
    locations = get_office_locations()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        cars = cars.filter(Q(title__icontains=keyword)
                           | Q(description__icontains=keyword)
                           | Q(attributes__value__icontains=keyword)).distinct()

    if 'brand' in request.GET:
        brand = request.GET['brand']
        cars = cars.filter(Q(brand__iexact=brand)).distinct()

    if 'model' in request.GET:
        model = request.GET['model']
        cars = cars.filter(Q(model__iexact=model)).distinct()

    if 'location' in request.GET:
        location = request.GET['location']
        all_offices = Office.objects.all()
        filtered_offices = [office for office in all_offices if office.get_address() == location]
        cars = cars.filter(address__in=filtered_offices).distinct()

    if 'year' in request.GET:
        year = request.GET['year']
        cars = cars.filter(Q(year__iexact=year)).distinct()

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']

        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'locations': locations,
        **car_values
    }
    return render(request, 'cars/search.html', context=data)
