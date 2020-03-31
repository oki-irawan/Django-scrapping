from django import forms

class LinkForm (forms.Form) :
    input_Link = forms.URLField(
        label = 'Input Link Product',
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'eg : https://fabelio.com/ip/mark-c-table.html',
                
            }
        )
    )