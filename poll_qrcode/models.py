from django.db import models
import qrcode
import io 
from django.core.files import File
from PIL import Image, ImageDraw

# 
# Create your models here.
class Qrcode(models.Model):
    name = models.CharField(max_length=200)
    qrcode = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (300, 300), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = io.BytesIO
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
