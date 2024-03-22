from django.db import models

class Provider(models.Model):
    Provider_ID = models.CharField(primary_key=True,max_length=200)
    Provider_Short_Name = models.CharField(max_length=40)
    Provider_Name = models.CharField(max_length=120, null=False, blank=False)
    def __str__(self):
       return str(self.Provider_ID)
