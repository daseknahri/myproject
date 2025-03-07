from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import admin
from unfold.sites import UnfoldAdminSite
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _, gettext, get_language
from unfold.decorators import action
from rent.forms import RatingForm
from .views import admin_dashboard
from .models import BusinessExpenditure, Car, City, Client, Reservation, CarExpenditure, Payment, Driver, ExpenditureType
from django.utils.html import format_html
from django import forms
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from unfold.admin import ModelAdmin
from .views import rate_client  # Import the view





@staff_member_required
def revenue_report(request):
    """
    Custom view for displaying revenue and expenditure report.
    """
    # Group reservations by month and calculate revenue
    data = (
        Reservation.objects.annotate(month=TruncMonth('start_date'))
        .values('month')
        .annotate(
            total_revenue=Sum('total_cost'),
            total_expenditures=Sum('car__expenditures__cost'),
        )
        .order_by('month')
    )
    return render(request, 'admin/revenue_report.html', {'data': data})
class DriverAdminForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'

    # Override the default widget for image fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_of_birth'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })
        self.fields['driver_license_year'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })

        self.fields['identity_card_front'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['identity_card_back'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['driver_license_front'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['driver_license_back'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['passport_image'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    # Override the default widget for image fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_of_birth'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })
        self.fields['driver_license_year'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })
        self.fields['identity_card_front'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['identity_card_back'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['driver_license_front'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['driver_license_back'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        self.fields['passport_image'].widget.attrs.update({'capture': 'camera', 'accept': 'image/*'})
        if not self.instance.pk:
                self.fields['total_amount_paid'].widget = forms.HiddenInput()
                self.fields['total_amount_due'].widget = forms.HiddenInput()
        else:
                self.fields['total_amount_paid'].widget.attrs['readonly'] = True
                self.fields['total_amount_due'].widget.attrs['readonly'] = True
                
class CarAdminForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    # Override the default widget for image fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
                self.fields['total_expenditure'].widget = forms.HiddenInput()
        else:
                self.fields['total_expenditure'].widget.attrs['readonly'] = True

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        '''widgets = {
            'pickup_time': forms.TextInput(attrs={
                'class': 'timepicker',  # Apply the timepicker class
                'placeholder': 'Select Time'  # Optional placeholder
            }),
            'dropoff_time': forms.TextInput(attrs={
                'class': 'timepicker',  # Apply the timepicker class
                'placeholder': 'Select Time'  # Optional placeholder
            }),
        }'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })
        self.fields['end_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'unfold-datepicker'  # Add a custom class for easier styling and JS interaction
        })
        if not self.instance.pk:
                self.fields['end_milage'].widget = forms.HiddenInput()
                self.fields['total_paid'].widget = forms.HiddenInput()
                self.fields['payment_status'].widget = forms.HiddenInput()
                self.fields['dropoff_time'].widget = forms.HiddenInput()
                self.fields['total_cost'].widget.attrs['readonly'] = True

        else:
            # If it's an existing object (editing), you can modify the form
            self.fields['total_paid'].widget.attrs['readonly'] = True
            self.fields['payment_status'].widget.attrs['readonly'] = True


@admin.action(description=_("Delete selected objects"))
def custom_delete_selected(modeladmin, request, queryset):
    with transaction.atomic():  # Ensure database integrity
        for obj in queryset:
            obj.delete()  # Call the model's delete() method

class CustomAdminSite(UnfoldAdminSite):
    
    SITE_header = _("Car Rental Management")
    site_title = _("TWINS T.B CAR")
    site_logo = "images/logo.png"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('revenue-report/', self.admin_view(revenue_report), name='revenue_report'),
        ]
        return custom_urls + urls
    def get_context(self, request):
        context = super().get_context(request)
        context['lang_code'] = get_language()  # Ensure the current language is passed
        return context
    def index(self, request, extra_context=None):
        context = super().each_context(request)
        context.update(admin_dashboard(request))
        if request.path == reverse('admin:index'):  # Check if it's the dashboard
            extra_context = extra_context or {}
            extra_context['custom_links'] = [
                {'url': reverse('revenue_report'), 'name': _("Revenue Report")},
            ]
            
        return super().index(request, context)
    
    def app_index(self, request, app_label, extra_context=None):
        """Display the app index page, listing all models."""
        context = {
            **self.each_context(request),
            "title": _("Dashboard"),
            "app_label": app_label,
            **(extra_context or {}),
        }
        return TemplateResponse(request, self.app_index_template or "admin/app_index.html", context)
    
    def each_context(self, request):
        context = super().each_context(request)
        # Add app_list to the context for all pages
        return context

admin_site = CustomAdminSite(name='custom_admin')

@admin.register(Driver, site=admin_site)
class DriverAdmin(ModelAdmin):
   # class Media:
    #    js = ('https://code.jquery.com/jquery-3.6.0.min.js', 'admin/js/custom_admin.js',)
    form = DriverAdminForm
    list_display = ('name', 'phone_number', 'license_age')
    search_fields = ('name', 'identity_card_number') 
    actions = [custom_delete_selected]
    fieldsets = (
        (_('Driver Information'), {
            'fields': ('name', 'phone_number', 'address', 'date_of_birth', 'driver_license_year', 'identity_card_number', 'driver_license_number')
        }),
        (_('documents'), {
            'fields': ('identity_card_front', 'identity_card_back', 'driver_license_front', 'driver_license_back', 'passport_image')
        }),
    )


### INLINE FOR EXPENDITURES IN CARS ###
class CarExpenditureInline(admin.TabularInline):
    model = CarExpenditure
    extra = 1  # Allows admin to add expenditures directly in the car interface
    readonly_fields = ('date',)  # Prevent editing the date
    classes = ('collapse',)

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0  # Prevent adding new reservations from the car page
    readonly_fields = ('total_cost', 'payment_status', 'total_paid')
    fields = ('total_cost', 'total_paid', 'start_date', 'end_date')  # Include all fields
    classes = ('collapse',)  # Optional: Add collapsible behavior
from unfold.decorators import display
### CAR ADMIN ###
@admin.register(Car, site=admin_site)
class CarAdmin(ModelAdmin):
    form = CarAdminForm
    #change_form_template = "admin/car_view.html"
    list_display = ('brand', 'model', 'plate_number', 'number_of_mile', 'total_expenditure',"availability_status")
    list_filter = ('daily_rate', 'is_available',)  # Filter by car brand and year
    search_fields = ('plate_number', 'brand',)  # Search by plate number, brand, or model
 #   inlines = [CarExpenditureInline, ReservationInline]  # Add expenditures inline
    actions = [custom_delete_selected]

    
    fieldsets = (
        (_('Car Information'), {
            'fields': ('brand', 'model', 'plate_number', 'year', 'image', 'daily_rate', 'number_of_mile')
        }),
        (_('Expenditure'), {
            'fields': ('total_expenditure',)
        }),
    )
    def availability_status(self, obj):
        if obj.is_available:
            return mark_safe('<span style="color: green;">✅</span>')
        return mark_safe('<span style="color: red;">❌</span>')

    availability_status.short_description = _("Available")
    def get_actions(self, request):
        # Call the parent method to get all actions
        actions = super().get_actions(request)
        # Remove the default delete action
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

### CLIENT ADMIN ###
@admin.register(Client, site=admin_site)
class ClientAdmin(ModelAdmin):
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', 'admin/js/custom_admin.js',)
    form = ClientAdminForm
    list_display = ('name', 'phone_number', 'display_rating', 'total_amount_paid', 'total_amount_due', 'age','license_age')
    search_fields = ('name', 'identity_card_number')  # Search by username, email, or phone
    list_filter = ('rating',)
    actions = [custom_delete_selected]
    fieldsets = (
        (_('Client Information'), {
            'fields': ('name', 'phone_number', 'address', 'date_of_birth', 'driver_license_year', 'identity_card_number', 'driver_license_number')
        }),
        (_('documents'), {
            'fields': ('identity_card_front', 'identity_card_back', 'driver_license_front', 'driver_license_back', 'passport_image')
        }),
        (_('Payment Details'), {
            'fields': ('total_amount_paid', 'total_amount_due')
        }),
    )

    def get_actions(self, request):
        # Call the parent method to get all actions
        actions = super().get_actions(request)
        # Remove the default delete action
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


### INLINE FOR PAYMENTS IN RESERVATIONS ###
class PaymentInline(admin.StackedInline):
    model = Payment
    fields = ("amount",)
    extra = 1  # Allows admin to add payments directly in the reservation interface



### RESERVATION ADMIN ###
@admin.register(Reservation, site=admin_site)
class ReservationAdmin(ModelAdmin):
    form = ReservationForm
    list_display = ('pk', 'car', 'client', 'start_date', 'end_date', 'total_cost', 'total_paid', 'status')
    autocomplete_fields = ['drivers', 'client']
    list_filter = ('payment_status', 'start_date', 'end_date')  
    search_fields = ('car__plate_number', 'client__name')  
    #readonly_fields = ('total_cost', 'payment_status', 'total_paid', 'pdf_link')  
    #inlines = [PaymentInline]  
    actions = [custom_delete_selected, "mark_as_picked_up", "mark_as_returned"]
    actions_row = ["pdf_linkk"]

    change_form_template = "admin/rent/reservation/change_form.html"
    fieldsets = (
        (_("Reservation Details"), {  # Translated Section Title
            'fields': ('car', 'client', 'drivers', 'actual_daily_rate')
        }),
        (_("Time and Location Details"), {  # Translated Section Title
            'fields': ('start_milage', 'end_milage', 'pickup_adresse' , 'dropoff_adresse', 'start_date', 'pickup_time','end_date', 'dropoff_time')
        }),
        (_("Payment Information"), {  # Translated Section Title
            'fields': ('total_paid', 'total_cost', 'payment_status')
        }),
    )

    class Media:
        js = ('admin/js/calculate_total_cost.js',)
    def mark_as_picked_up(self, request, queryset):
        """ Admin action: Mark reservation as 'In Progress' and update pickup time. """
        for reservation in queryset:
            if reservation.status != "in_progress":
                reservation.pickup_time = now().time()
                reservation.status = "in_progress"
                reservation.car.is_available = False
                reservation.car.number_of_mile = reservation.start_milage
                reservation.car.save(update_fields=['is_available','number_of_mile'])
                reservation.save()

        self.message_user(request, _("The Vehicle Marked as Deliverd."))

    mark_as_picked_up.short_description = _("Mark as Delivred")
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("rate-client/<int:reservation_id>/", self.admin_site.admin_view(rate_client), name="rate-client"),
        ]
        return custom_urls + urls  # Custom URLs must come first
    @action(description=_("Mark as Returned"), url_path="mark-as-returned")
    def mark_as_returned(self, request, queryset):
        # **1️⃣ Ensure queryset is not empty**
        if not queryset.exists():
            self.message_user(request, _("No reservations selected."), level="warning")
            return redirect("admin:rent_reservation_changelist")

        # **2️⃣ Only process reservations that are not already completed**
        reservations_to_update = queryset.exclude(status="completed")

        if not reservations_to_update.exists():
            self.message_user(request, _("All selected reservations are already completed."), level="info")
            return redirect("admin:rent_reservation_changelist")

        # **3️⃣ Show rating form only if there's one reservation**
        if reservations_to_update.count() == 1:
            reservation = reservations_to_update.first()
            return redirect(reverse("admin:rate-client", args=[reservation.id]))

        for reservation in reservations_to_update:
            reservation.dropoff_time = now().time()
            reservation.status = "completed"
            reservation.car.is_available = True
            reservation.car.save(update_fields=["is_available"])
            reservation.save()

        self.message_user(request, _("Selected reservations marked as returned."))
        return redirect("admin:rent_reservation_changelist")

    @action(description=_("Download PDF Receipt"), url_path="download-pdf-receipt")
    def pdf_linkk(self, request, object_id):
        """Serve the PDF receipt for download."""
        reservation = self.get_object(request, object_id)
        
        # Generate the PDF if it's not already done
        reservation.generate_pdf_receipt()

        # Open the PDF file (adjust the path if needed)
        file_path = reservation.pdf_receipt.path

        # Serve the file as HTTP response
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename={reservation.pdf_receipt.name}'
            return response


    def get_actions(self, request):
        """Override get_actions to remove default delete and use a custom delete action."""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


### PAYMENT ADMIN ###
@admin.register(Payment, site=admin_site)
class PaymentAdmin(ModelAdmin):
    list_display = ('reservation', 'amount', 'payment_date')
    list_filter = ('payment_date',)  # Filter by payment date
    search_fields = ('reservation__car__plate_number', 'reservation__client__name')  # Search by car or client
    #readonly_fields = ('payment_date',)  # Prevent editing payment date
    actions = [custom_delete_selected]

    fieldsets = (
        (_('Payment Details'), {
            'fields': ('reservation', 'amount', 'payment_date')
        }),
    )
    def get_actions(self, request):
        # Call the parent method to get all actions
        actions = super().get_actions(request)
        # Remove the default delete action
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


### CAR EXPENDITURE ADMIN ###
@admin.register(CarExpenditure, site=admin_site)
class CarExpenditureAdmin(ModelAdmin):
    list_display = ('car', 'description', 'cost', 'date')
    list_filter = ('date', 'car')  # Filter by expenditure date
    search_fields = ('car__name', 'description')  # Search by car plate number or description
    #readonly_fields = ('date',)  # Prevent editing the date
    actions = [custom_delete_selected]

    fieldsets = (
        (_('Expenditure Information'), {
            'fields': ('car', 'description', 'cost', 'date')
        }),
    )
    def get_actions(self, request):
        # Call the parent method to get all actions
        actions = super().get_actions(request)
        # Remove the default delete action
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(BusinessExpenditure, site=admin_site)
class BusinessExpenditureAdmin(ModelAdmin):
    list_display = ('type', 'amount', 'date')
    list_filter = ('type',)
    search_fields = ('type',"date")

@admin.register(ExpenditureType, site=admin_site)
class ExpenditureTypeAdmin(ModelAdmin):
    pass
@admin.register(City, site=admin_site)
class CityAdmin(ModelAdmin):
    pass



admin_site.register(User, UserAdmin)
