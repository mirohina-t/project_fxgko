from django import forms
from .models import Starts, StartsСategory, Sportsmens, Treners, StartsDetails, SportItem

class RegistrationForm(forms.Form):
    # Категория (выбирается из доступных для этого соревнования)
    category = forms.ModelChoiceField(
        queryset=StartsСategory.objects.none(), 
        label="Категория участников",
        widget=forms.Select(attrs={'id': 'category-select'})
    )
    
    # Данные спортсмена
    sportsmen_last_name = forms.CharField(max_length=50, label="Фамилия спортсмена")
    sportsmen_first_name = forms.CharField(max_length=50, label="Имя спортсмена")
    sportsmen_year = forms.IntegerField(label="Год рождения", min_value=1900, max_value=2026)
    sportsmen_category = forms.IntegerField(label="Спортивный разряд", min_value=0)
    
    # Данные тренера
    trener_last_name = forms.CharField(max_length=50, label="Фамилия тренера")
    trener_first_name = forms.CharField(max_length=50, label="Имя тренера")
    trener_patronymic = forms.CharField(max_length=50, required=False, label="Отчество тренера")
    trener_email = forms.EmailField(label="Email тренера")
    trener_phone = forms.CharField(max_length=20, label="Телефон тренера")
    
    def __init__(self, *args, **kwargs):
        start = kwargs.pop('start', None)
        super().__init__(*args, **kwargs)
        if start:
            self.start = start
            self.fields['category'].queryset = start.category_of_starts.all()