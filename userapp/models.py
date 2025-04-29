from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'notification'

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.TextField()
    messages = models.TextField()
    status = models.TextField()
    activity_record = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'activities'

