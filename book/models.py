from django.db import models

# Create your models here.





class Books(models.Model):

    name=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    genre=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="images",null=True,blank=True)
    language=models.CharField(max_length=200,null=True)

    

    def __str__(self):
        return self.name