from PIL import Image
from django.core.files import File
from io import BytesIO

class ImageResizeMixin:
    def resize_image(self, image, size=(800, 800)):  # Default size (800x800)
        img = Image.open(image)
        img = img.convert('RGB')  # Ensure it's in RGB format
        
        img.thumbnail(size)  # Resize the image to the thumbnail size
        
        # Save the resized image to memory
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        
        # Create a new Django file-like object
        new_image = File(thumb_io, name=image.name)
        return new_image
