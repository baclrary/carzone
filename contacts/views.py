from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect

from contacts.models import Contact


def inquiry(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        car_id = request.POST["car_id"]
        car_title = request.POST["car_title"]
        customer_need = request.POST["customer_need"]
        state = request.POST["state"]
        city = request.POST["city"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        user_id = request.POST["user_id"]

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request,
                               "You have already made an inquiry for this car. Please, wait until we get back to you")
                return redirect('/cars/' + car_id)

        contact = Contact(car_id=car_id, car_title=car_title, user_id=user_id, first_name=first_name,
                          last_name=last_name, customer_need=customer_need, state=state, city=city,
                          email=email, phone=phone,
                          message=message)
        contact.save()

        admins = get_user_model().objects.filter(is_superuser=True)
        send_mail('New car inquiry',
                  f"You have a new inquiry for the {car_title}.\nYou may check details into admin panel",
                  "carzone@customers.com", [admin.email for admin in admins], fail_silently=False)

        messages.success(request, message="Inquiry successfully created and will be proceed soon")
        return redirect('/cars/' + car_id)
