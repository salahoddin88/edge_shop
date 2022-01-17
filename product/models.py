from django.db import models


class ProductCategory(models.Model):
    """ Product Category Model """
    name = models.CharField(max_length=150)
    status = models.BooleanField(default=True)

    def __str__(self):
        """ String representation for object ProductCategory object(1) -> self.name (SmartPhone)"""
        return str(self.name)


class Product(models.Model):
    """ Product Model """
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="ProductCategory")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=1)
    cover_image = models.ImageField()
    status = models.BooleanField(default=True)

    def __str__(self):
        """ String representation for object Product object(1) -> self.name (S21 FE)"""
        return str(self.name)


class ProductImage(models.Model):
    """ Product will have more than one image """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        """ String representation for object ProductImage object(1) -> self.product (S21 FE)"""
        return str(self.product)

