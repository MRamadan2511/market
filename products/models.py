from django.db import models
from django.urls import reverse
from accounts.models import User
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


from .mixins import ImageResizeMixin
from ecommerce.utils import unique_slug_generator

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="%(class)s_created", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="%(class)s_updated", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk and user:  # Object is being created
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)



class Market(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # Location info or use a geolocation field
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(BaseModel, ImageResizeMixin):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # Optional logo
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("category_detail", kwargs={"slug": self.slug})

        
    def save(self, *args, **kwargs):
        # If the product has an image, resize it
        if self.logo:
            self.logo = self.resize_image(self.logo)

        # Generate a slug from the name if it’s not already set
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Check if the slug already exists and modify it
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super(Category, self).save(*args, **kwargs)


# def category_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

# pre_save.connect(category_pre_save_receiver, sender=Category) 


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)  # Optional logo

    def __str__(self):
        return self.name



class ProductUnit(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  


class PackingUnit(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     


class Product(BaseModel):
    # sku = models.CharField(max_length=100, unique=True)  # Global SKU
    name = models.CharField(max_length=255)  # Default product name
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional product image
    description = models.TextField(blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit  = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, null=True,blank=True)
    packing_unit  = models.ForeignKey(PackingUnit, on_delete=models.SET_NULL, null=True,blank=True)

    # Additional attributes
    weight = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)  # Weight in kg or other units
    dimensions = models.CharField(max_length=255, blank=True)  # Optional dimensions (e.g., "10x5x3 cm")
    expiration_date = models.DateField(blank=True, null=True)  # If applicable (for perishable goods)

    def __str__(self):
        return f"{self.name} - {self.weight}{self.unit}"
    

    @property
    def best_price_profile(self):
        """
        Get the ProductProfile with the lowest price for this product.
        """
        return ProductProfile.objects.filter(product=self).order_by('price').first()

    @property
    def best_price(self):
        """
        Get the lowest price for this product.
        """
        best_profile = self.best_price_profile
        return best_profile.price if best_profile else None


        # Add this method to resize the image
    def resize_image(self, image, size=(800, 800)):  # Default size (800, 800)
        img = Image.open(image)
        img = img.convert('RGB')  # Ensure it's in RGB format
        
        img.thumbnail(size)  # Resize the image to the thumbnail size
        
        # Save the resized image to memory
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        
        # Create a new Django file-like object
        new_image = File(thumb_io, name=image.name)
        return new_image

    # Override the save method
    def save(self, *args, **kwargs):
        # If the product has an image, resize it
        if self.image:
            self.image = self.resize_image(self.image)
        
        # Call the parent class save method to save to the database
        print("okay")
        super(Product, self).save(*args, **kwargs)




class ProductProfile(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    # Supermarket-specific attributes
    market_name = models.CharField(max_length=255, blank=True, null=True)  # Custom name at this market
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Stock level at the supermarket
    last_updated = models.DateTimeField(auto_now=True)  # To track price/stock updates

    # Optional additional fields
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)  # Availability at this specific market
    promotional_text = models.CharField(max_length=255, blank=True, null=True)  # Promotion-specific info
    shelf_location = models.CharField(max_length=255, blank=True)  # Specific shelf info in the store

    # Track important dates like promotions or stock history
    promotion_start_date = models.DateField(blank=True, null=True)
    promotion_end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'market')  # Ensures uniqueness for product-market combination

    def __str__(self):
        return f"{self.get_display_name()} at {self.market.name}"

    def get_display_name(self):
        """
        Return the market-specific name if available, otherwise fall back to the default product name.
        """
        return f"{self.product.name}-{self.product.weight}{self.product.unit}" if self.market_name else f"{self.product.name}-{self.product.weight}{self.product.unit}"

    def get_final_price(self):
        """
        Calculate the price after applying any available discount.
        """
        if self.discount:
            return self.price - self.discount
        return self.price
    
    @classmethod
    def get_best_price(cls, product):
        """
        Get the lowest price for a given product.
        """
        lowest_price_profile = cls.objects.filter(product=product).order_by('price').first()
        return lowest_price_profile

    @classmethod
    def get_best_price_market(cls, product):
        """
        Get the lowest price for a given product.
        """
        best_price_market = cls.objects.filter(product=product).order_by('price').first().market_name
        return best_price_market
        


