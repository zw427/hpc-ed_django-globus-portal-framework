from django import forms

class ExcelFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if not file.name.endswith(('.xls', '.xlsx')):
            raise forms.ValidationError('Only .xls and .xlsx files are allowed.')

        if file.size > 1 * 1024 * 1024:
            raise forms.ValidationError('File size must be under 1MB.')
        
        return file
