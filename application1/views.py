from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import VehicleEntry,Category
from application1.forms import LoginForm
from application1.models import login as LoginModel
from django.core.paginator import Paginator
import random
from django.http import JsonResponse

def index (request):
    return render(request, 'index.html')


# PASTE HERE
def category(request):

    if request.method == "POST":

        area_number = request.POST.get('area_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_limit = request.POST.get('vehicle_limit')
        parking_charge = request.POST.get('parking_charge')

        Category.objects.create(
            area_number=area_number,
            vehicle_type=vehicle_type,
            vehicle_limit=vehicle_limit,
            parking_charge=parking_charge
        )

        return redirect('category')

    # ✅ THIS MUST BE INSIDE FUNCTION
    data_list = Category.objects.all().order_by('id')

    paginator = Paginator(data_list, 10)

    page_number = request.GET.get('page')

    data = paginator.get_page(page_number)

    return render(request, 'category.html', {'data': data})


def delete_category(request, id):

    item = get_object_or_404(Category, id=id)

    item.delete()

    return redirect('category')


def edit_category(request, id):

    item = get_object_or_404(Category, id=id)

    if request.method == "POST":

        item.area_number = request.POST.get('area_number')
        item.vehicle_type = request.POST.get('vehicle_type')
        item.vehicle_limit = request.POST.get('vehicle_limit')
        item.parking_charge = request.POST.get('parking_charge')

        item.save()

        return redirect('category')

    data = Category.objects.all()

    return render(request, 'category.html', {
        'data': data,
        'item': item
    })
def toggle_category(request, id):

    item = get_object_or_404(Category, id=id)

    # toggle True ↔ False
    item.status = not item.status
    item.save()

    return redirect('category')


def dashboard(request):

    parked = VehicleEntry.objects.filter(status="Parked").count()

    departed = VehicleEntry.objects.filter(status="Leaved").count()

    categories = Category.objects.count()

    total_records = VehicleEntry.objects.count()

    total_earnings = VehicleEntry.objects.aggregate(
        total=Sum('charge')
    )['total'] or 0

    total_slots = Category.objects.aggregate(
        total=Sum('vehicle_limit')
    )['total'] or 0

    return render(request, 'dashboard.html', {

        'parked': parked,
        'departed': departed,
        'categories': categories,
        'total_records': total_records,
        'total_earnings': total_earnings,
        'total_slots': total_slots
    })
def entry1 (request):
    return render(request, 'entry1.html')
def reports(request):

    searched_ids = request.session.get('searched_ids', [])

    vehicle_number = request.GET.get('vehicle_number')

    if vehicle_number:

        vehicle = VehicleEntry.objects.filter(
            vehicle_number=vehicle_number
        ).first()

        if vehicle and vehicle.id not in searched_ids:
            searched_ids.append(vehicle.id)

            request.session['searched_ids'] = searched_ids

    vehicles = VehicleEntry.objects.filter(
        id__in=searched_ids
    )

    receipt_id = request.GET.get('receipt')

    receipt = None

    if receipt_id:

        receipt = VehicleEntry.objects.filter(
            id=receipt_id
        ).first()

    return render(request, 'reports.html', {
        'vehicles': vehicles,
        'receipt': receipt
    })
def settings (request):
    return render(request, 'settings.html')
def vehicle_entry(request):

    categories = Category.objects.filter(status=True)

    if request.method == "POST":

        vehicle_number = request.POST.get('vehicle_number')
        category_id = request.POST.get('vehicle_type')

        category = Category.objects.get(id=category_id)

        VehicleEntry.objects.create(
            vehicle_number=vehicle_number,
            vehicle_type=category,
            area_no=category.area_number,
            charge=category.parking_charge,
            status="Parked",
            action="Parked"
        )

        return redirect('vehicle_entry')

    vehicle_list = VehicleEntry.objects.all().order_by('id')

    paginator = Paginator(vehicle_list, 10)

    page_number = request.GET.get('page')

    vehicles = paginator.get_page(page_number)

    return render(request, 'vehicle_entry.html', {
        'categories': categories,
        'vehicles': vehicles
    })
def vehicle_number(request):

    vehicles = VehicleEntry.objects.all()

    if 'searched_ids' not in request.session:
        request.session['searched_ids'] = []

    searched_ids = request.session['searched_ids']

    vehicle_number = request.GET.get('vehicle_number')

    if vehicle_number:

        vehicle = VehicleEntry.objects.filter(
            vehicle_number=vehicle_number
        ).first()

        if vehicle:

            # Remove if already exists
            if vehicle.id in searched_ids:
                searched_ids.remove(vehicle.id)

            # Add to top
            searched_ids.insert(0, vehicle.id)

            request.session['searched_ids'] = searched_ids

    searched_vehicle = VehicleEntry.objects.filter(
        id__in=searched_ids
    )

    searched_vehicle = sorted(
        searched_vehicle,
        key=lambda x: searched_ids.index(x.id)
    )

    return render(request, 'vehicle_number.html', {
        'vehicles': vehicles,
        'searched_vehicle': searched_vehicle
    })
def clear_vehicle_search(request):

    request.session['searched_ids'] = []

    return redirect('vehicle_number')
def remove_vehicle_search(request, id):

    ids = request.session.get('searched_ids', [])

    if id in ids:
        ids.remove(id)

    request.session['searched_ids'] = ids

    return redirect('vehicle_number')

def user_login(request):
    form=LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            mobilenumber = form.cleaned_data['mobilenumber']
            password = form.cleaned_data['password']

            user = LoginModel.objects.filter(
                username=username,
                mobilenumber=mobilenumber,
                password=password
            ).first()

            if user:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Username,mobilenumber or Password")

    return render(request, 'index.html', {'form': form})
def forgot_password(request):

    if request.method == "POST":

        mobilenumber = request.POST.get('mobilenumber')

        user = LoginModel.objects.filter(
            mobilenumber=mobilenumber
        ).first()

        # MOBILE NUMBER FOUND
        if user:

            otp = random.randint(100000, 999999)

            print("OTP IS :", otp)

            # SAVE OTP IN SESSION
            request.session['otp'] = str(otp)
            request.session['mobile'] = mobilenumber
            request.session.modified = True

            return JsonResponse({
                "otp_sent": True
            })

        # WRONG MOBILE NUMBER
        else:

            return JsonResponse({
                "otp_sent": False,
                "message": "Wrong Mobile Number"
            })

    return JsonResponse({
        "otp_sent": False
    })
def manage(request):

    if request.method == "POST":

        category = Category.objects.get(id=request.POST['vehicle_type'])

        VehicleEntry.objects.create(
            vehicle_number=request.POST['vehicle_number'],
            vehicle_type=category,
            area_no=category.area_number,
            charge=category.parking_charge,
            status="Parked",
            action="register"
        )

        return redirect('manage')

    vehicle_list = VehicleEntry.objects.all().order_by('id')

    paginator = Paginator(vehicle_list, 10)

    page_number = request.GET.get('page')

    vehicles = paginator.get_page(page_number)

    return render(request, 'manage.html', {
        'vehicles': vehicles
    })
def toggle_vehicle_status(request, id):

    vehicle = get_object_or_404(VehicleEntry, id=id)

    if vehicle.status == "Parked":

        vehicle.status = "Leaved"
        vehicle.action = "Leaved"

    else:

        vehicle.status = "Parked"
        vehicle.action = "Parked"

    vehicle.save()

    return redirect('manage')


def otp_verify(request):
    return render(request, 'otp_verify.html')
def otp_verify(request):
    return render(request, 'otp_verify.html')
def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        session_otp = request.session.get('otp')

        if entered_otp == session_otp:

            return JsonResponse({
                "success": True
            })

        else:

            return JsonResponse({
                "success": False
            })
def reset_password(request):

    if request.method == "POST":

        new_password = request.POST.get('new_password')
        mobilenumber = request.session.get('mobile')

        print("SESSION:", mobilenumber)
        print("PASSWORD:", new_password)

        if not mobilenumber:
            return JsonResponse({"success": False, "message": "Session expired"})

        if not new_password:
            return JsonResponse({"success": False, "message": "Password empty"})

        user = LoginModel.objects.filter(mobilenumber=mobilenumber).first()

        if user:
            user.password = new_password
            user.save()

            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "message": "User not found"})
def search_vehicle(request):
    vehicle_number = request.GET.get('vehicle_number', '')

    vehicles = VehicleEntry.objects.filter(
        vehicle_number__icontains=vehicle_number
    )

    data = []

    for v in vehicles:

        data.append({
            'id': v.id,
            'vehicle_number': v.vehicle_number,
            'vehicle_type': str(v.vehicle_type),
            'area_no': v.area_no,
            'charge': str(v.charge),
            'status': v.status
        })

    return JsonResponse(data, safe=False)