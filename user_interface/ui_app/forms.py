from django import forms
from .models import Products

#class UploadFileForm(forms.ModelForm):
#    class Meta:
#        model = Products
#        fields = ['product_name', 'fat', 'carbohydrate', 'protein']
#        labels = {'product_name': 'product', }
#        widject = {
#            'product_name': forms.TextInput(attrs={
#                'max_length': '100'
#            })
#        }

class UploadFileForm(forms.Form):
     file = forms.FileField() # for creating file input  

