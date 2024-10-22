import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product, Brand, Category, ProductUnit, PackingUnit, ProductProfile, Market
from django.core.files import File
from django.conf import settings
import os
from accounts.models import User

class Command(BaseCommand):
    help = 'Load products from an Excel file'


    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID for the created_by field')
    
    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)  # Get the user object based on the provided ID

        file_path = os.path.join(settings.BASE_DIR, 'products_list.xlsx')
        self.import_products(file_path, user)

    def import_products(self, file_path, user):
        # Read Excel file
        df = pd.read_excel(file_path)

        # Loop over the rows and create products
        for index, row in df.iterrows():
            try:
                brand = Brand.objects.get(name=row['brand_name']) if pd.notna(row['brand_name']) else None
                category = Category.objects.get(name=row['category_name']) if pd.notna(row['category_name']) else None

                # Handle cases where multiple ProductUnits exist by using filter
                unit = ProductUnit.objects.filter(name=row['unit_name']).first() if pd.notna(row['unit_name']) else None
                packing_unit = PackingUnit.objects.filter(name=row['packing_unit_name']).first() if pd.notna(row['packing_unit_name']) else None
                
                # Create or update the Product
                product, created = Product.objects.update_or_create(
                    name=row['name'],
                    weight=row['weight'], 
                    brand = brand,
                    unit=unit,
                    defaults={
                        # 'description': row['description'],
                        'category': category,
                        'packing_unit': packing_unit,
                        'created_by': user,
                        # 'dimensions': row['dimensions'],
                        # 'expiration_date': row['expiration_date'],
                        
                    }
                )

                # Optionally, handle the image file upload
                if pd.notna(row['image']):
                    print("ok")
                    image_path = os.path.join(settings.BASE_DIR, 'media/products/', row['image'])
                    print(image_path)
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as image_file:
                            product.image.save(row['image'], File(image_file), save=True)

                print(f"Product '{product.name}' with weight '{row['weight']}' has been {'created' if created else 'updated'}.")

                # Now create ProductProfile for the specified market
                market_name = row['market']  # Assuming your Excel has this column
                market = Market.objects.get(name=market_name)  # You may want to handle cases where the market does not exist

                ProductProfile.objects.update_or_create(
                    product=product,
                    market=market,
                    defaults={
                        'market_name': row['pro_name_market'],  # Assuming price is also in your Excel file
                        'price': row['price'],  # Assuming price is also in your Excel file
                        'stock': row['stock'],  # Assuming stock is also in your Excel file
                        'created_by': user,
                    }
                )

                print(f"ProductProfile for '{product.name}' in market '{market.name}'  has been {'created' if created else 'updated'}.")

            except Exception as e:
                print(f"Error processing row {index}: {e}")

