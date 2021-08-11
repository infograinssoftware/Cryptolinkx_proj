from django.db import models
from users.models import Custom_User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class User_OTP(models.Model):
    user = models.ForeignKey(Custom_User, related_name='custom_user_otp', on_delete = models.CASCADE)
    email = models.EmailField(max_length = 50)
    otp = models.IntegerField()

    def __str__(self):
        return f'{self.email} with {self.otp}'
              

class User_qrcode(models.Model):
    user = models.ForeignKey(Custom_User, on_delete = models.CASCADE)
    qr_code = models.ImageField(null = True, blank = True)
    otp = models.IntegerField()

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.otp)
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.otp}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

DOC_TYPE = (
    ('SSN','SSN'),
    ('PASSPORT','PASSPORT'),
    ('DRIVING_LICENSE','DRIVING_LICENSE'),
)

class User_KYC(models.Model):
    user = models.ForeignKey(Custom_User, on_delete = models.CASCADE)
    document_type = models.CharField(max_length = 20, choices = DOC_TYPE ,default = 'SSN')
    id_number = models.IntegerField()
    doc_front_img  = models.ImageField(null = True, blank = True)
    doc_back_img = models.ImageField(null = True, blank = True) 
    doc_selfie = models.ImageField(null = True, blank = True)

    def __str__(self):
        return f'{self.id_number}-------->{self.user}'