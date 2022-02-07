from django.shortcuts import render, redirect
from django.views import View
from product.models import ProductCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as AuthLogin, logout as AuthLogout


class Login(View):

    template_name = 'login.html'
    form_class = AuthenticationForm
    navigationProductCategories = ProductCategory.objects.filter(status=True)

    def get(self, request):
        
            
        form = self.form_class()
        context = {
            'navigationProductCategories' : self.navigationProductCategories,
            'form' : form,
            'next' : request.GET.get('next')
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            AuthLogin(request, form.get_user())
            if request.POST.get('next') != 'None':
                return redirect(request.POST.get('next'))
            return redirect('HomePage')
        context = {
            'navigationProductCategories' : self.navigationProductCategories,
            'form' : form
        }
        return render(request, self.template_name, context)


def logout(request):
    AuthLogout(request)
    return redirect('HomePage')
