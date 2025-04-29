from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from retailer.models import * 
from userapp.models import * 
from base.models import * 
import os,base64
from django.contrib.auth.decorators import login_required
from datetime import datetime,date,timedelta
from django.db.models import Avg

# Create your views here.
def buisness_list(request):
    # print(request.user)
    context = {"latest_question_list": 'latest_question_list'}
    return render(request, "buisness.html", context)

def Createbuisness(request):
    from django.shortcuts import render
from .models import buisness
import os


def your_form_view(request):
    if request.method == "POST":
        # Extract form data
        print('enter')
        email = request.POST.get('username')
        buisness_name = request.POST.get('buisness') 
        user_name = request.POST.get('user_name') 
        phone = request.POST.get('phone')
        buisness_profile_ = request.FILES.get('buisness_profile_')
        service1 = request.POST.get('service1')
        print(user_name)
        service2 = request.POST.get('service2')
        service3 = request.POST.get('service3')
        service4 = request.POST.get('service4')
        haircut_price = request.POST.get('haircut_price')
        massage_price = request.POST.get('massage_price')
        beard_price = request.POST.get('beard_price')
        haircolor_price = request.POST.get('haircolor_price')
        buisness_address = request.POST.get('buisness_address')
        city = request.POST.get('city')
        buisness_profile = request.FILES.get('buisness_profile')
        buisness_profile0 = request.FILES.get('buisness_profile0')
        buisness_profile1 = request.FILES.get('buisness_profile1')
        buisness_profile2 = request.FILES.get('buisness_profile2')
        buisness_profile3 = request.FILES.get('buisness_profile3')
        buisness_profile4 = request.FILES.get('buisness_profile4')
        buisness_profile5 = request.FILES.get('buisness_profile5')
        password = request.POST.get('password')
        print('enter read')
        # Process form data
        
        services = ','.join(filter(None, [service1, service2, service3, service4]))
        services_prices = ','.join(filter(None, [haircut_price, massage_price, beard_price, haircolor_price]))
        
        # Save remaining business profiles in another folder
        remaining_profiles = [buisness_profile, buisness_profile0, buisness_profile1,
                              buisness_profile2, buisness_profile3, buisness_profile4, buisness_profile5]

        url = r"D:\hanumanta\Ezcut"
        directory_name = buisness_name
        directory_path = os.path.join(url, directory_name)

        # Check if the directory exists, if not, create it
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created at {directory_path}")

        try:
            # Open the uploaded file and write it to the destination directory
            with open(os.path.join(directory_path, f"{buisness_name}.jpg"), 'wb+') as destination:
                for chunk in buisness_profile_.chunks():
                    destination.write(chunk)
            print(f"Image saved successfully at: {directory_path}")

        except Exception as e:
            print(f"Error saving image: {e}")

        for idx, profile in enumerate(remaining_profiles):
            if profile:
                try:
                    with open(os.path.join(directory_path, f"profile_{idx}.jpg"), 'wb+') as destination:
                        for chunk in profile.chunks():
                            destination.write(chunk)
                        print(f"Profile {idx} saved successfully at: {directory_path}")
                except Exception as e:
                    print(f"Error saving profile {idx}: {e}")
        print('enter here')
        # Save data to the database
        buisness.objects.using("EZCUT").create(
            email_id=email, buisness_name=buisness_name, user_name=user_name, phone=phone, city=city, shop_address=buisness_address,
            services=services, services_price=services_prices, password_user=password
        )

        context = {"message": "User created successfully!"}
        return render(request, "base.html", context)

    else:
        # Render the form for GET requests
        return render(request, "base.html")
    
import json
from django.http import JsonResponse   
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def set_appointment(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        print(user_id)
        try:
            data = json.loads(request.body)
            cart_list = data.get('cartList', [])
            cart_total = data.get('cartTotal', 0)
            date_ = data.get('date_', '')
            time_ = data.get('time_', '')
            shop_id = data.get('shop_id', '')
            services = []
            for item in cart_list:
                service, price = item.split(' - ')
                services.append(service)
            print("Services:", services)
            services_string = ', '.join(services)
            print(services_string)
            date_time=datetime.now()
            retail_data=list(buisness.objects.using("EZCUT").filter(id=shop_id).values_list('buisness_name','shop_address','city','phone'))
            if schedule.objects.using("EZCUT").filter(shop_id=shop_id,date=date_,time=time_).exists()==True:
                return JsonResponse({'data': 'Appointment not set '})
            else:
                notification_message=f"Your Appointment Set to date : {date_}, time : {time_} , in shop :{retail_data[0][0]}, Address : {retail_data[0][1]}, City : {retail_data[0][2]}"
                schedule.objects.using('EZCUT').create(shop_id=shop_id,user_id=user_id,services=services_string,total_price=cart_total,time=time_,date=date_,status="PENDING",appointment_record=date_time)
                Activity.objects.using("EZCUT").create(user_id=user_id, messages=notification_message,status="PROCEED")
                return JsonResponse({'data': 'Appointment set successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'data': 'Your Not Login'})
    
from django.shortcuts import render
from django.db.models import Avg
import os
import base64
def get_shoptemplates(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        base_directory = r"D:\hanumanta\Ezcut"

        # Fetch shop data
        shop_data = list(buisness.objects.using("EZCUT").filter(user_id=user_id).values_list(
            'id', 'eamil_id', 'buisness_name', 'user_name', 'phone', 'city',
            'services', 'services_price', 'shop_address'
        ))

        shop_id = shop_data[0][0]
        if schedule.objects.using("EZCUT").filter(shop_id=shop_id).exists()==True :
            # Fetch shop appointments
            shop_appointments = list(schedule.objects.using("EZCUT").filter(shop_id=shop_id, status="PENDING").values_list(
                'user_id', 'services', 'time', 'date','id'
            ))

            # Fetch user information for each appointment
            appointment_details = []
            for appointment in shop_appointments:
                user_id_ = appointment[0]
                user_info = list(UserForm.objects.using("EZCUT_USER").filter(id=user_id_).values_list(
                    'username', 'first_name', 'last_name','phone'
                ))
                encoded_image = None
                if user_info:
                    username = user_info[0][0]
                    directory_path = os.path.join(base_directory, username)

                    if os.path.isdir(directory_path):
                        image_path = os.path.join(directory_path, f"{username}.jpg")
                        if os.path.isfile(image_path):
                            with open(image_path, "rb") as image_file:
                                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                appointment_details.append({
                    'appointment': appointment,
                    "encoded_image": encoded_image,
                    'user_info': user_info[0]
                })
            today = date.today()
            far_future_date = today + timedelta(days=7)
            shop_schedule = list(schedule.objects.using("EZCUT").filter(date__range=(today, far_future_date),shop_id=shop_id, status="ACCEPT").order_by("date","time").values_list(
                'user_id', 'services', 'time', 'date','id'
            ))

            # Fetch user information for each appointment
            schedule_details = []
            for appointment in shop_schedule:
                user_id_ = appointment[0]
                user_info = list(UserForm.objects.using("EZCUT_USER").filter(id=user_id_).values_list(
                    'username', 'first_name', 'last_name','phone'
                ))
                encoded_image = None
                if user_info:
                    username = user_info[0][0]
                    directory_path = os.path.join(base_directory, username)

                    if os.path.isdir(directory_path):
                        image_path = os.path.join(directory_path, f"{username}.jpg")
                        if os.path.isfile(image_path):
                            with open(image_path, "rb") as image_file:
                                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                schedule_details.append({
                    'appointment': appointment,
                    "encoded_image": encoded_image,
                    'user_info': user_info[0]
                })

            # Calculate ratings
            rating_count, average_rating = calculate_rating(shop_id)
            rating = [rating_count, average_rating]

            # Get encoded images
            profile_directory = os.path.join(base_directory, str(shop_data[0][2]))
            image_files = get_encoded_images(profile_directory)

            # Render the template with the context data
            return render(request, "retailers.html", {
                "shop_data": shop_data,
                "image_files": image_files,
                'rating': rating,
                'appointment_details': appointment_details,
                'schedule_details': schedule_details
            })
        else:
            url = reverse('get_shop_datails') + f'?shop_id={shop_id}'
            return redirect(url)
    else:
        return redirect("sign_in_form")

def calculate_rating(shop_id):
    """
    Calculate the count of reviews and the average rating for a given shop_id.
    """
    reviews = review.objects.using('EZCUT').filter(shop_id=shop_id)
    rating_count = reviews.count()
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    return rating_count, avg_rating

def get_encoded_images(profile_directory):
    """
    Get base64 encoded images from the profile directory.
    """
    image_files = []
    for filename in os.listdir(profile_directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            with open(os.path.join(profile_directory, filename), "rb") as file:
                encoded_image = base64.b64encode(file.read()).decode('utf-8')
                image_files.append(encoded_image)
    return image_files

@csrf_exempt
def conformation(request):
    if request.method == "POST":
        conformation = request.POST.get('apoointment')
        text = request.POST.get('text') 
        user_id = request.POST.get('user_id') 
        today = date.today()
        time_= datetime.now().strftime('%H:%M:%S')
        schedule.objects.using("EZCUT").filter(id=user_id).update(status=conformation,remarks=text)
        user_from_schedule=list(schedule.objects.using("EZCUT").filter(id=user_id).values_list('user_id'))
        print(user_from_schedule)
        notification_message = f'Your appointment status is {conformation}. Remarks: {text}'
        Notification.objects.using("EZCUT").create(user_id=user_from_schedule[0][0], message=notification_message)
        Activity.objects.using("EZCUT").create(user_id=user_from_schedule[0][0], messages=notification_message,status="PROCEED")

        context={"data" : "Done"}
        return JsonResponse(context)
    
@csrf_exempt
def settel_appointment(request):
    if request.method == "POST":
        conformation = request.POST.get('apoointment')
        text = request.POST.get('text') 
        user_id = request.POST.get('user_id') 
        today = date.today()
        time_= datetime.now().strftime('%H:%M:%S')
        schedule.objects.using("EZCUT").filter(id=user_id).update(status=conformation,remarks=text)
        user_from_schedule=list(schedule.objects.using("EZCUT").filter(id=user_id).values_list('user_id'))
        print(user_from_schedule)
        notification_message = f'Your appointment status is {conformation}. Remarks: {text}'
        Notification.objects.using("EZCUT").create(user_id=user_from_schedule[0][0], message=notification_message)
        Activity.objects.using("EZCUT").create(user_id=user_from_schedule[0][0], messages=notification_message,status="PROCEED")

        context={"data" : "Done"}
        return JsonResponse(context)
    
