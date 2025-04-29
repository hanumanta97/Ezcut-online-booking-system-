from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.utils.timezone import localdate
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from base.models import *
from retailer.models import *
from django.db.models import Avg
import os,base64
from django.contrib import messages
from django.contrib.auth import login,logout
from django.http import request
from django.contrib.auth.hashers import make_password,check_password


def index(request):
    context = {"latest_question_list": 'latest_question_list'}
    return redirect('get_shops')

def index2(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        buisness_login=''
        shop_data=get_shops_data()
        profile_data = list(UserForm.objects.using('EZCUT_USER').filter(id=user_id).values_list('username', 'email'))
        if buisness.objects.using("EZCUT").filter(user_id=user_id).exists()==True:
            buisness_login='yes'
        else:
            buisness_login='no'
        try:
            base_url = r"D:\hanumanta\Ezcut"
            username = profile_data[0][0]
            directory_path = os.path.join(base_url, username)
           
            if os.path.isdir(directory_path):
                image_path = os.path.join(directory_path, f"{username}.jpg")
                if os.path.isfile(image_path):
                    with open(image_path, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    context = {
                        "username": profile_data[0][0],
                        "email": profile_data[0][1],
                        "user_id":user_id,
                        "encoded_image": encoded_image,
                        "shop_data": shop_data,
                        "buisness_login":buisness_login
                    }
                    return render(request, "loginbase.html", context)
                else:
                    context = {
                        "username": profile_data[0][0],
                        "email": profile_data[0][1],
                        "user_id":user_id,
                        "encoded_image": 'encoded_image',
                        "shop_data": shop_data,
                        "buisness_login":buisness_login
                    }
                    return render(request, "loginbase.html", context)
            else:
                context = {
                    "username": profile_data[0][0],
                    "email": profile_data[0][1],
                    "user_id":user_id,
                    "encoded_image": 'encoded_image',
                        "shop_data": shop_data,
                        "buisness_login":buisness_login
                }
                return render(request, "loginbase.html", context)
        except Exception as e:
            pass
    else:
        return HttpResponseRedirect(reverse('sign_in_form'))
    
                
def signout(request):
    user_id = request.session['user_id']
    print(user_id)
    logout(request)
    return redirect("index")

def buisness_list(request):
    context = {"latest_question_list": 'latest_question_list'}
    return render(request, "buisness.html", context)

def sign_in_form(request):
    context = {"latest_question_list": 'latest_question_list'}
    return render(request, "index.html", context)

def images_reder(request):
    filtered_profiles = UserForm.objects.filter(id=13)  # Adjust the filter criteria as needed
    return render(request, 'image.html', {'profiles': filtered_profiles})

def filtered_profile_view(request):
    print('kfkf')


def backtobase(request):
    if  request.session:
        user_id = request.session['user_id']
        print(user_id)
        context = {"latest_question_list": 'latest_question_list'}
        return render(request, "base.html", context)
    else:
        return HttpResponseRedirect(reverse('sign_in_form'))

def checkUser(request):
    if request.method == "POST":
        email = request.POST.get('username').strip()
        password = request.POST.get('password')
        try:
            user_form = UserForm.objects.using("EZCUT_USER").get(email=email)
        except UserForm.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("sign_in_form")
        if check_password(password, user_form.password):
            request.session['user_id'] = user_form.id 
            return redirect("index2")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("sign_in_form")
    else:
        return render(request, "index.html")
            

def CreateUser(request):
    if request.method == "POST":
        First_name = request.POST.get('First_Name')
        Last_name = request.POST.get('Last_Name') 
        username = request.POST.get('username') 
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')
        password = request.POST.get('password')
        profile = request.FILES.get('profile')
        hashed_password = make_password(password)
        password=hashed_password
        url = r"D:\hanumanta\Ezcut"
        directory_name = username
        directory_path = os.path.join(url, directory_name)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created at {directory_path}")

        try:
            with open(os.path.join(directory_path, f"{username}.jpg"), 'wb+') as destination:
                for chunk in profile.chunks():
                    destination.write(chunk)
            print(f"Image saved successfully at: {directory_path}")

        except Exception as e:
            print(f"Error saving image: {e}")

        UserForm.objects.using("EZCUT_USER").create(
            first_name=First_name, last_name=Last_name, username=username,
            email=email, phone=phone, city=city, address=address,
            password=password, profile=profile
        )
        context = {"message": "User created successfully!"}
        return render(request, "base.html", context)
    


def Createbuisness(request):
    if request.method == "POST":
        email = request.POST.get('username')
        buisness_name = request.POST.get('business_name')
        user_name = request.POST.get('user_name')
        First_name = request.POST.get('first_name')
        Last_name = request.POST.get('last_name') 
        phone = request.POST.get('phone')
        buisness_profile = request.FILES.get('buisness_profile')  # corrected field name
        service1 = request.POST.get('service1')
        service2 = request.POST.get('service2')
        service3 = request.POST.get('service3')
        service4 = request.POST.get('service4')
        haircut_price = request.POST.get('haircut_price')
        massage_price = request.POST.get('massage_price')
        beard_price = request.POST.get('beard_price')
        haircolor_price = request.POST.get('haircolor_price')
        buisness_address = request.POST.get('address')
        buisness_profile0 = request.FILES.get('buisness_images')
        buisness_profile1 = request.FILES.get('buisness_images0')
        buisness_profile2 = request.FILES.get('buisness_images1')
        buisness_profile3 = request.FILES.get('buisness_images2')
        buisness_profile4 = request.FILES.get('buisness_images3')
        city = request.POST.get('city')  
        password = request.POST.get('password')
        hashed_password = make_password(password)
        password=hashed_password
        latest_id = buisness.objects.using("EZCUT").latest('id').id
        i=latest_id+1
        services = ','.join(filter(None, [service1, service2, service3, service4]))
        services_prices = ','.join(filter(None, [haircut_price, massage_price, beard_price, haircolor_price]))
        try:
            base_directory = r"D:\hanumanta\Ezcut"
            profile_directory = os.path.join(base_directory, "EZCUT_PROFILES")
            directory_name = buisness_name
            directory_user = user_name
            directory_path = os.path.join(base_directory, directory_name)
            directory_path_ = os.path.join(base_directory, directory_user)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            if not os.path.exists(directory_path_):
                os.makedirs(directory_path_)
            
            with open(os.path.join(directory_path_, f"{user_name}.jpg"), 'wb+') as destination:
                for chunk in buisness_profile.chunks():
                    destination.write(chunk)

            with open(os.path.join(directory_path, f"{buisness_name}_primary.jpg"), 'wb+') as destination:
                for chunk in buisness_profile.chunks():
                    destination.write(chunk)

            with open(os.path.join(profile_directory, f"{str(i)}_primary.jpg"), 'wb+') as destination:
                for chunk in buisness_profile.chunks():
                    destination.write(chunk)

            for index, image in enumerate([buisness_profile0, buisness_profile1, buisness_profile2, buisness_profile3, buisness_profile4], start=1):
                if image:
                    with open(os.path.join(directory_path, f"{buisness_name}_additional_{index}.jpg"), 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)

        except Exception as e:
            print(f"Error saving image: {e}")

        UserForm.objects.using("EZCUT_USER").create(
            first_name=First_name, last_name=Last_name, username=user_name,
            email=email, phone=phone, city=city, address=buisness_address,
            password=password
        )
        latest_id_buisness = UserForm.objects.using("EZCUT_USER").latest('id').id
        buisness.objects.using("EZCUT").create(
            eamil_id=email, buisness_name=buisness_name, user_name=user_name, phone=phone,
            shop_address=buisness_address,city=city, services=services, services_price=services_prices,
            password_user=password,user_id=latest_id_buisness
        )

        context = {"message": "User created successfully!"}
        return redirect('index2')
    else:
        return render(request, "base.html")

def get_shops_data():
    base_directory = r"D:\hanumanta\Ezcut"
    profile_directory = os.path.join(base_directory, "EZCUT_PROFILES")

    # Ensure that the directory exists
    if os.path.isdir(profile_directory):
        # List all files in the directory
        files = os.listdir(profile_directory)
        # Filter image files
        image_files = [file for file in files if file.lower().endswith(('.png','.jpg','.jpeg','.gif','.bmp'))]

        # Initialize an empty list to store image data
        shop_data = []

        # Iterate over each shop data
        for data in buisness.objects.using('EZCUT').values_list('id','buisness_name','shop_address','city'):
            # Generate image file path for the current shop
            image_path = os.path.join(profile_directory, f"{data[0]}_primary.jpg")

            # Check if the image file exists
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    # Read and encode the image
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                rating_count, average_rating = calculate_rating(data[0])
                rating = [rating_count, average_rating]
                print(rating)
                # Create a dictionary with shop data and encoded image
                context = {
                    "id":data[0],
                    "buisness_name": data[1],
                    "shop_address": data[2],
                    "city": data[3],
                    'rating': rating,
                    "encoded_image": encoded_image
                }
                # Append the dictionary to shop_data list
                shop_data.append(context)
        
        # Render the template with shop_data
        return shop_data
def get_shops(request):
    base_directory = r"D:\hanumanta\Ezcut"
    profile_directory = os.path.join(base_directory, "EZCUT_PROFILES")

    # Ensure that the directory exists
    if os.path.isdir(profile_directory):
        # List all files in the directory
        files = os.listdir(profile_directory)
        # Filter image files
        image_files = [file for file in files if file.lower().endswith(('.png','.jpg','.jpeg','.gif','.bmp'))]

        # Initialize an empty list to store image data
        shop_data = []

        # Iterate over each shop data
        for data in buisness.objects.using('EZCUT').values_list('id','buisness_name','shop_address','city'):
            # Generate image file path for the current shop
            image_path = os.path.join(profile_directory, f"{data[0]}_primary.jpg")

            # Check if the image file exists
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    # Read and encode the image
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                rating_count, average_rating = calculate_rating(data[0])
                rating = [rating_count, average_rating]
                print(rating)
                # Create a dictionary with shop data and encoded image
                context = {
                    "id":data[0],
                    "buisness_name": data[1],
                    "shop_address": data[2],
                    "city": data[3],
                    'rating': rating,
                    "encoded_image": encoded_image
                }
                # Append the dictionary to shop_data list
                shop_data.append(context)
        
        # Render the template with shop_data
        return render(request, "base.html", {"shop_data": shop_data})

import os
import base64


def get_shop_data(shop_id):
    """
    Fetch shop data from the database based on shop_id.
    """
    return get_object_or_404(buisness.objects.using("EZCUT").values(
        'id', 'eamil_id', 'buisness_name', 'user_name', 'phone', 'city',
        'services', 'services_price', 'shop_address'
    ), id=shop_id)

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

def get_shop_datails(request):
    if request.method == "GET":
        shop_id = request.GET.get('shop_id')
        base_directory = r"D:\hanumanta\Ezcut"

        # Fetch shop data
        shop_data = get_shop_data(shop_id)

        if shop_data:
            # Convert shop_data to a dictionary
            shop_data_dict = dict(shop_data)
            services_list = shop_data_dict['services'].split(',')
            services_prices_list = shop_data_dict['services_price'].split(',')

            # Add services and prices to shop_data_dict
            shop_data_dict['services_and_prices'] = [{'service': service, 'price': price} for service, price in zip(services_list, services_prices_list)]

            # Calculate rating
            rating_count, average_rating = calculate_rating(shop_id)
            rating = [rating_count, average_rating]

            profile_directory = os.path.join(base_directory, str(shop_data_dict['buisness_name']))
            image_files = get_encoded_images(profile_directory)
            
            return render(request, "shop.html", {"shop_data": shop_data_dict, "image_files": image_files, 'rating': rating ,'products': products})
        else:
            return render(request, "error.html", {"message": "Shop not found."})
        

def get_review(request):
    if request.method == "POST":
        shop_id = request.POST.get('shop_id') 
        rating = request.POST.get('rating') 
        comment = request.POST.get('comment')  
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            # user_name=list(UserForm.objects.using('EZCUT_USER').filter(id=user_id).values_list('username'))
            user_name = UserForm.objects.using('EZCUT_USER').filter(id=user_id).values_list('username', flat=True).first()

            print(user_name)
            review.objects.using("EZCUT").create(shop_id=shop_id,rating=rating,usermessage=comment,username=user_name)
            data='yes'
            return JsonResponse({'data':data})
        else:
            data='no'
            return JsonResponse({'data':data})
        


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})