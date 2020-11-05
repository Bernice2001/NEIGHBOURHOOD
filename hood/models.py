from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Hood(models.Model):   
    hood_name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.hood_name
    

class Neighbourhood(models.Model): 
    neighbourhood = models.ForeignKey(Hood, on_delete=models.CASCADE, related_name='hood')  
    location = models.CharField(max_length=120, default='Kenya')
    population = models.IntegerField(default=0)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_name', default=1)
    
    def __str__(self):
        return self.neighbourhood.hood_name
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
        
    def find_neighbourhood(self, pk):
        hood = get_object_or_404(Neighbourhood, id=pk)
        return Neighbourhood.objects.filter(Neighbourhood=hood)
    
    @classmethod
    def update_neighbourhood(cls, id, value):
        cls.objects.filter(id=id).update(population=value)
        
    @classmethod
    def update_count(cls, id, value):
        cls.objects.filter(id=id).update(population=value).count()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=120)
    hood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
        

class Business(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='job_description')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='business_user')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    business_email = models.EmailField(max_length=254)
    
    def __str__(self):
        return self.name
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
        
    def find_business(self, pk):
        work = get_object_or_404(Business, id=pk)
        return Business.objects.filter(name=work)
   
    @classmethod
    def update_business(cls, id, value):
        cls.objects.filter(id=id).update(name=value)
        
    @classmethod
    def search_business(cls,search_term):
        job = Business.objects.filter(name__icontains=search_term)
        return job
    
class Post(models.Model):
    image = CloudinaryField('image')
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=1000, verbose_name='Description')
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='your_profile')
    neighbour = models.ForeignKey(Hood, on_delete=models.CASCADE, related_name='neighbour_name')  
    
    def __str__(self):
        return self.title

    