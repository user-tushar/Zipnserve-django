from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=120, unique=True) # slug is nothing but url of that product.
    description = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='images/category', blank=True) # image/category = inside image folder create category folder and save the img there.. and blank = True  means ... this field is optional ... even it is blank still it won't give error.

    class Meta: # this is for correct the model name in admin pannel.
        verbose_name = 'category' # by default string Representatio of our object model name in admin pannel is this..
        # but when we add our model to admin pannel it convert into plural form by adding a 's'.

        verbose_name_plural = 'categories' # our model is "category" .. in admin pannel string Representatio is convert into "categorys" which is wrong spell .. so, here we are tried to correct that spell string Representatio by giving correct name  as "categories"


    def slug_url (self): # this is used to display the url  when 'slug_url' calls in webpage.
            return reverse('items_by_category', args = [self.slug] )


    def __str__(self):
        return self.category_name
    
# modification as required .

# we changed slug = charfield to .. slugfield 
# '''
# this will prepopulate category slug.
# means :  it will accept slug url automatically we don't need to write it.
# '''