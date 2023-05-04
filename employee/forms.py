from django import forms

from .models import Employee


class AddEmployeeForm(forms.ModelForm):
    phone = forms.CharField(max_length=12, widget=forms.NumberInput())
    joined_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'

        # Set custom text for the first option of department field
        self.fields['department'].empty_label = 'Select Department'
        # Set custom text for the first option of role field
        self.fields['role'].empty_label = 'Select Role'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['required'] = True
