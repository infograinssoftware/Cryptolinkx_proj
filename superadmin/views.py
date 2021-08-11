from django.shortcuts import render

# Create your views here.
def cryptolinkx_admin(request):
    return render(request, 'superadmin/dashboard.html')