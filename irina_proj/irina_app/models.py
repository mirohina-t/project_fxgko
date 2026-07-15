from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
    

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="autored_news") # related_name="posts" некое виртуальное поле, через которое мы можем достучаться до всех постов нашего Юзера
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=10_000)
    publish_date = models.DateTimeField(auto_now_add=True) # при создании записи время укажется автоматически (auto_now_add=True)
    
    def clean(self):
        # Проверяем, является ли автор superuser'ом
        if not self.author.is_superuser:
            raise ValidationError({'author': 'Автором поста может быть только superuser.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем метод clean для валидации
        super().save(*args, **kwargs)

    def __str__(self)-> str:
        return f"{self.author.username}; {self.title}"
    
    class Meta:
        verbose_name = "Новость"    
        verbose_name_plural = "Новости" 
    

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="news/", blank=False, null=False)

    def __str__(self):
        return f"Картинка для {self.news.title}"
    

class Starts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="autored_starts") 
    name =  models.CharField(max_length=200, verbose_name="Название")
    event_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    registration_end_date = models.DateField(verbose_name="Дата окончания регистрации")
    description =  models.CharField(max_length=200, verbose_name="Описание")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")

    def clean(self):
        # Проверяем, является ли автор superuser'ом
        if not self.author.is_superuser:
            raise ValidationError({'author': 'Автором поста может быть только superuser.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем метод clean для валидации
        super().save(*args, **kwargs)

    def __str__(self) -> str:
            return f"{self.name}, {self.event_date}"
    
    def is_registration_open(self):
        return timezone.now().date() <= self.registration_end_date
    
    def is_event_in_future(self):
        return timezone.now().date() < self.event_date
    
    class Meta:
        verbose_name = "Соревнование"    
        verbose_name_plural = "Соревнования" 
        ordering = ['event_date', 'registration_end_date']   

class SportItem(models.Model):
    name = models.CharField(max_length=50, help_text="Предмет")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class StartsСategory(models.Model):
    title =  models.CharField(max_length=250, help_text="Название")
    starts = models.ForeignKey(Starts, on_delete=models.CASCADE, related_name='category_of_starts')
    available_items = models.ManyToManyField(SportItem, related_name='categories', blank=True, help_text="Доступные предметы для этой категории")

    def __str__(self):
        return f"{self.title} ({self.starts.name})"
    
    class Meta:
        verbose_name = "Категория участников"
        verbose_name_plural = "Категории участников"
    

class Treners(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, default="")

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}; {self.email}"
    

class Sportsmens(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    year = models.SmallIntegerField(help_text="Год рождения")
    sport_category = models.SmallIntegerField(help_text="Разряд")
    trener = models.ForeignKey(Treners, on_delete=models.SET_NULL, null=True, blank=True, related_name='sportsmens_of_trener')

    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}; {self.year}; {self.sport_category}"
 



class SportGroups(models.Model):
    name = models.CharField(max_length=10, help_text="Группа")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name

class StartsDetails(models.Model):
    starts = models.ForeignKey(Starts, on_delete=models.CASCADE, related_name='detail_of_starts')
    sportsmam = models.ForeignKey(Sportsmens, on_delete=models.CASCADE, related_name='participation_details')
    sport_item = models.ForeignKey(SportItem, on_delete=models.CASCADE, help_text="Выбранный предмет" )
    item_music = models.FileField(upload_to='audio/%Y/%m/', verbose_name="Файл (MP3)")
    starts_category = models.ForeignKey(StartsСategory, on_delete=models.SET_NULL, null=True, blank=True)
    sport_groupe = models.ForeignKey(SportGroups, on_delete=models.SET_NULL, null=True, blank=True)
     

    def __str__(self) -> str:
        return f"{self.sportsmam.last_name} {self.sportsmam.first_name} - {self.sport_item.name}"
    


class FederationInfo(models.Model):
    """
    Модель для хранения общей информации о федерации.
    """
    president_name = models.CharField(max_length=255, verbose_name="Имя президента")
    president_birth_date = models.DateField(verbose_name="Дата рождения президента")
    president_bio = models.TextField(verbose_name="Биография президента")
    president_photo = models.ImageField(upload_to='president_photos/', blank=True, null=True, verbose_name="Фото президента")

    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return f"Информация о Федерации ({self.president_name})"

    class Meta:
        verbose_name = "Информация о Федерации"
        verbose_name_plural = "Информация о Федерации"

    