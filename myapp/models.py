from django.db import models
from django.db.models import Model

# Create your models here.
from django.contrib.auth.models import AbstractUser

#中略

class CustomUser(AbstractUser):
    icon = models.FileField(default='/')
    #追加するフィールドやバリデーションなど。

class Data(Model):
    talk = models.CharField(max_length=500)
    talk_from = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="send_data_set"
    )
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_data_set")
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
# class FileUpload(models.Model):
#     upload = models.FileField(upload_to='media_local/%Y/%m/%d', verbose_name='添付ファイル')