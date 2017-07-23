from django.forms import ModelForm
from order.models import Item 

class ItemForm(ModelForm):
    class Meta:
        model = Item
        labels = {
            'quantity': ''
        }
        fields = ('quantity', )
