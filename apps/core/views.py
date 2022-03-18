from django.shortcuts import render

# Global Name
user_name = "Solomon Bestz"

# Create your views here.
def landingpage(request):
    return render(request, 'main/landingpage.html', {'name':user_name})

# Create contact view
def contact(request):
    return render(request, 'main/contact.html', {'name': user_name})
    