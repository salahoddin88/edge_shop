from django.shortcuts import render
from django.views import View
from product.models import ProductCategory


class HomePage(View):

    def get(self, request):
        navigationProductCategories = ProductCategory.objects.filter(status=True)
        productCategories = ProductCategory.objects.filter(status=True).order_by('-id')[:3]
        context = {
            'navigationProductCategories' : navigationProductCategories,
            'productCategories' : productCategories
        }
        return render(request, 'home-page.html', context)


