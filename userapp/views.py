import time
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from userapp.models import *
from django.shortcuts import render,redirect
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from base.models import *
from retailer.models import *
import os,base64
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect

@csrf_exempt
def check_notifications(request):
    if request.method == "POST":
        userID = request.POST.get('userID')
        if Notification.objects.using("EZCUT").filter(user_id=userID).exists():
            messages= Notification.objects.using("EZCUT").filter(user_id=userID).order_by("-created_at").first()
            data=messages.message
            messages.delete()
            # d_count=delete_notifications()
            context={"data" : data}
            return JsonResponse(context)
        else :
            context={"data" : "NO data"}
            return JsonResponse(context)


def delete_notifications():
    # Assuming you want to delete notifications older than a certain date
    # For example, deleting notifications older than 30 days:
    from_date = timezone.now() - timedelta(days=30)
    
    # Delete notifications for a specific user and older than from_date
    notifications_to_delete = Notification.objects.filter( Q(created_at__lt=from_date)
    )
    
    deleted_count, _ = notifications_to_delete.delete()
    
    return deleted_count

def get_mails(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        buisness_login=''
        profile_data = list(UserForm.objects.using('EZCUT_USER').filter(id=user_id).values_list('username', 'email'))
        if buisness.objects.using("EZCUT").filter(user_id=user_id).exists()==True:
            buisness_login='yes'
        else:
            buisness_login='no'
        if Activity.objects.using("EZCUT").filter(user_id=user_id,status="PROCEED").exists()==True:
            userInfo=list(Activity.objects.using("EZCUT").filter(user_id=user_id,status="PROCEED").values_list('id','messages','activity_record').order_by("-activity_record"))
            print(userInfo[0][2])
        else:
            userInfo=''
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
                        "userInfo": userInfo,
                        "buisness_login":buisness_login
                    }
                    return render(request, "inbox.html", context)
                else:
                    context = {
                        "username": profile_data[0][0],
                        "email": profile_data[0][1],
                        "user_id":user_id,
                        "encoded_image": 'encoded_image',
                        "userInfo": userInfo,
                        "buisness_login":buisness_login
                    }
                    return render(request, "inbox.html", context)
            else:
                context = {
                    "username": profile_data[0][0],
                    "email": profile_data[0][1],
                    "user_id":user_id,
                    "encoded_image": 'encoded_image',
                    "userInfo": userInfo,
                        "buisness_login":buisness_login
                }
                return render(request, "inbox.html", context)
        except Exception as e:
            pass
    else:
        return HttpResponseRedirect(reverse('sign_in_form'))

@csrf_exempt    
def delete_msg(request):
    if request.method == "POST":
        userID = request.POST.get('id')

        Activity.objects.using("EZCUT").filter(id=userID).update(status="DELETED")
        context={"data" : 'data'}
        return JsonResponse(context)
