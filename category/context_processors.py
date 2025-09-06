from .models import Category

def menu_links (request):
    links = Category.objects.all()
    return dict(link = links) # we use this context processors 
# coz we want to use this context often so , we create context 
# here links is value in dict and link is key .. so key will be called in html