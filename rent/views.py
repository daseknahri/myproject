from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Count, F, Q
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth

from rent.helper import calculate_rental_days_for_months
from .models import Car, City, Reservation, Client, Payment, BusinessExpenditure, CarExpenditure, CustomerInfo
from django.http import JsonResponse
from django.utils.translation import get_language
from collections import defaultdict
from django.utils.translation import gettext as _
from django.utils.formats import date_format


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .forms import RatingForm


def rate_client(request, reservation_id):
    """
    Handles the rating form submission for a returned reservation.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        print("DEBUG: Received POST Data:", request.POST)  # 👀 Check what is received

        form = RatingForm(request.POST)
        if form.is_valid():
            print("DEBUG: Form is valid!")  # 👀 If this is NOT printed, the form is invalid
            rating = int(form.cleaned_data["rating"])
            number_of_milage = int(form.cleaned_data["number_of_milage"])

            # ✅ Mark reservation as returned
            reservation.dropoff_time = now().time()
            reservation.status = "completed"
            reservation.end_milage = number_of_milage
            reservation.car.is_available = True
            reservation.car.number_of_mile = number_of_milage
            reservation.car.save(update_fields=["is_available","number_of_mile"])
            reservation.save()

            # ✅ Update client rating
            client = reservation.client
            existing_rating = client.rating or 5
            client.rating = (existing_rating + rating) / 2
            client.save()

            messages.success(request, _("Reservation marked as returned and client rated!"))
            return redirect("admin:rent_reservation_changelist")

        else:
            print("DEBUG: Form is INVALID! Errors:", form.errors)  # 👀 Log validation errors

    else:
        form = RatingForm(initial={"reservation_id": reservation.id})

    return render(request, "admin/rating_popup.html", {"form": form, "reservation": reservation})



def home(request):
    cities = City.objects.all()
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars, 'cities': cities})


@staff_member_required
def admin_dashboard(request):
    current_date = now().date()

    # --- Financial Data Calculation ---
    monthly_revenue_data = defaultdict(float)
    for reservation in Reservation.objects.all():
        start_date = reservation.start_date
        end_date = reservation.end_date
        daily_rate = reservation.actual_daily_rate or reservation.car.daily_rate

        # Check if the reservation is for one day
        if start_date == end_date:
            # If it's one day, just add one day of revenue
            days_in_month = 1
            month = start_date.replace(day=1)
            monthly_revenue_data[month] += days_in_month * float(daily_rate)
        else:
            while start_date < end_date:
                # Determine the month and the last day of the month
                month = start_date.replace(day=1)
                last_day_of_month = (month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                
                # Calculate the number of days in the current month (exclusive of end_date)
                days_in_month = (min(end_date, last_day_of_month) - start_date).days
                
                # Add the revenue for this period
                monthly_revenue_data[month] += days_in_month * float(daily_rate)
                
                # Move to the next month
                start_date = last_day_of_month + timedelta(days=1)

    # Convert to a list of dicts for better presentation
    monthly_revenue_data = [{'month': month, 'total_revenue': revenue} for month, revenue in monthly_revenue_data.items()]
    monthly_revenue_data.sort(key=lambda x: x['month'])

    # Handle expenditure data
    monthly_car_expenditure_data = CarExpenditure.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_expenditure=Sum('cost'))
    monthly_business_expenditure_data = BusinessExpenditure.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_expenditure=Sum('amount'))

    monthly_expenditure_data = defaultdict(float)
    for item in monthly_car_expenditure_data:
        monthly_expenditure_data[item['month']] += float(item['total_expenditure'])
    for item in monthly_business_expenditure_data:
        monthly_expenditure_data[item['month']] += float(item['total_expenditure'])

    # Combine revenue and expenditure data into a final financial report
    monthly_financial_data = [
        {
            'month': revenue_item['month'],
            'revenue': revenue_item['total_revenue'],
            'expenditure': monthly_expenditure_data[revenue_item['month']],
            'profit': revenue_item['total_revenue'] - monthly_expenditure_data[revenue_item['month']],
        }
        for revenue_item in monthly_revenue_data
    ]
    monthly_financial_data.sort(key=lambda x: x['month'])

    # --- Number of Reservations & Available Cars ---
    total_reservations = Reservation.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()

    # --- Profit & Expenses by Car ---
    car_profit_data = []
    for car in Car.objects.all():
        total_revenue = sum(
            reservation.rental_days * (reservation.actual_daily_rate or car.daily_rate)
            for reservation in car.reservations.all()
        )
        total_expense = CarExpenditure.objects.filter(car=car).aggregate(Sum('cost'))['cost__sum'] or 0
        profit = total_revenue - total_expense
        car_profit_data.append({
            'car': car,
            'total_revenue': total_revenue,
            'total_expense': total_expense,
            'profit': profit,
        })

    # --- Clients with Balance Due ---
    clients_with_due = Client.objects.filter(total_amount_due__gt=0)

    # 🛠️ **STRUCTURE TABLE DATA FOR UNFOLD**
    table_clients_with_due = {
        "headers": [_("Client"), _("Total Due")],
        "rows": [
            [client.name, f"{client.total_amount_due:.2f} MAD"]
            for client in clients_with_due
        ]
    }

    table_financial_data = {
        "headers": [_("Month"), _("Total Revenue"), _("Total Expenditure"), _("Profit")],
        "rows": [
            [
                item["month"].strftime("%B %Y"),
                f"{item['revenue']:.2f} MAD",
                f"{item['expenditure']:.2f} MAD",
                f"{item['profit']:.2f} MAD"
            ]
            for item in monthly_financial_data
        ]
    }

    table_car_profit_data = {
        "headers": [_("Car"), _("Total Revenue"), _("Total Expense"), _("Profit")],
        "rows": [
            [
                item["car"].model,
                f"{item['total_revenue']:.2f} MAD",
                f"{item['total_expense']:.2f} MAD",
                f"{item['profit']:.2f} MAD"
            ]
            for item in car_profit_data
        ]
    }
    # Car rental days for each month
    car_rental_days_data = []
    for car in Car.objects.all():
        rental_days_by_month = {}
        for reservation in car.reservations.all():
            start_date = reservation.start_date
            end_date = reservation.end_date

            # Split reservation into months
            while start_date < end_date:
                month = start_date.replace(day=1)
                
                # Determine the last day of the current month
                last_day_of_month = (month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                
                # Calculate the days in the current month (exclusive of end_date)
                days_in_month = (min(end_date, last_day_of_month) - start_date).days
                rental_days_by_month[month] = rental_days_by_month.get(month, 0) + days_in_month
                
                # Move to the next month
                start_date = last_day_of_month + timedelta(days=1)

        # Append data
        car_rental_days_data.append({
            'car': car,
            'rental_days_by_month': rental_days_by_month,
        })

    all_months = set()

    for car_data in car_rental_days_data:
        all_months.update(car_data["rental_days_by_month"].keys())

    # 🟢 Sort months for correct display
    all_months = sorted(all_months)
    translated_months = [date_format(month, "F Y") for month in all_months]


    # 🟢 Structure data for Unfold Table
    table_car_rental_days = {
        "headers": [_("Car")] + translated_months,  # Car Name + Months
        "rows": [
            [car_data["car"].model] + [str(car_data["rental_days_by_month"].get(month, 0)) for month in all_months]
            for car_data in car_rental_days_data
        ]
    }

    # --- Pass Data to Context ---
    context = {
        "table_car_rental_days" : table_car_rental_days,
        "table_clients_with_due": table_clients_with_due,
        "table_financial_data": table_financial_data,
        "table_car_profit_data": table_car_profit_data,
        "total_reservations": total_reservations,
        "available_cars": available_cars,
        "lang_code": get_language(),
    }

    return context



def get_car_daily_rate(request):
    """Return the daily rental rate of the selected car."""
    car_id = request.GET.get('car_id')
    if not car_id:
        return JsonResponse({"error": "Car ID not provided"}, status=400)

    try:
        car = Car.objects.get(id=car_id)
        return JsonResponse({"daily_rate": float(car.daily_rate),"number_of_milage": int(car.number_of_mile)})
    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)