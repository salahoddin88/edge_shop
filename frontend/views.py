from django.shortcuts import render
from django.views import View
from product.models import ProductCategory, Product, ProductImage


class HomePage(View):

    def get(self, request):
        navigationProductCategories = ProductCategory.objects.filter(status=True)
        productCategories = ProductCategory.objects.filter(status=True).order_by('-id')[:3]
        context = {
            'navigationProductCategories' : navigationProductCategories,
            'productCategories' : productCategories
        }
        return render(request, 'home-page.html', context)


class ProductListing(View):
    
    template_name = 'product-listing.html'

    def get(self, request, product_category_id=None):

        navigationProductCategories = ProductCategory.objects.filter(status=True)

        searchdict = {
            "status" : True
        }
        if product_category_id:
            searchdict['product_category_id'] = product_category_id

        if request.GET.get('search'):
            searchdict['name__icontains'] = request.GET.get('search')

        if request.GET.get('min'):
            searchdict['price__gte'] = request.GET.get('min').replace('₹', '')

        if request.GET.get('max'):
            searchdict['price__lte'] = request.GET.get('max').replace('₹', '')

        if request.GET.get('sorting'):
            if request.GET.get('sorting') == 'low':
                products = Product.objects.filter(**searchdict).order_by('price')
            if request.GET.get('sorting') == 'high':
                products = Product.objects.filter(**searchdict).order_by('-price')

        else:
            products = Product.objects.filter(**searchdict)

        
        context = {
            'navigationProductCategories' : navigationProductCategories,
            'products' : products, 
            'product_category_id' : product_category_id
        }
        return render(request, self.template_name, context)


class ProductDetails(View):
    template_name = 'product-details.html'

    def get(self, request, product_id):
        navigationProductCategories = ProductCategory.objects.filter(status=True)
        try:
            product = Product.objects.get(pk=product_id)
            relatedProducts = Product.objects.filter(status=True, product_category_id=product.product_category_id).exclude(id=product_id)
        except Product.DoesNotExist:
            product = {}
            relatedProducts = {}
        productImages = ProductImage.objects.filter(product_id=product_id)
        context = {
            'navigationProductCategories' : navigationProductCategories,
            'product' : product,
            'productImages' : productImages,
            'relatedProducts' : relatedProducts
        }
        return render(request, self.template_name, context)