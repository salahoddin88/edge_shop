from django.shortcuts import render
from django.views import View
from product.models import ProductCategory


class HomePage(View):

    def get(self, request):
        navigationProductCategory = ProductCategory.objects.filter(status=True)

        # productCategory = ProductCategory.objects.filter(status=True)[start:end-1]
        productCategory = ProductCategory.objects.filter(status=True).order_by('-id')[:3]
        print(productCategory)
        context = {
            'navigationProductCategory' : navigationProductCategory,
            'productCategory' : productCategory
        }
        return render(request, 'home-page.html', context)


