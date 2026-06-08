from django import forms


class ProductForm(forms.Form):
    title = forms.CharField(label='Наименование', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    category = forms.IntegerField(label='Категория', widget=forms.Select(attrs={'class': 'form-select'}))
    price = forms.DecimalField(label='Стоимость', max_digits=7, decimal_places=2, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    image_url = forms.URLField(label='Изображение', widget=forms.URLInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(label='Остаток', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)
        if categories is not None:
            self.fields['category'].widget.choices = [(c.pk, c.title) for c in categories]


class SearchForm(forms.Form):
    title = forms.CharField(label='Поиск', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по названию...'}))