from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from irina_app.forms import RegistrationForm
from irina_app.models import News, FederationInfo, NewsImage, Starts, StartsСategory, Sportsmens, Treners, StartsDetails, SportItem
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime


def index(request):
    return render(request, "irina_app/templates/index.html")            


def news_list(request):
    all_news = News.objects.all().order_by("-publish_date") # от большего к меньшему знак - от новых к старым
    paginator = Paginator(all_news, 2) # чтобы показывал 2 поста за раз , а не всю кучу
    page_number = request.GET.get("page_number", 1) # из reqest через GET запрос пытаемся получить то, что приходит по ключу "page_number", если ничего, пусть будет первая страница
    page_obj = paginator.get_page(page_number) # бурум нужную пачку постов из пагинатора

    context={"all_news": page_obj, "title": "news", "paginator": paginator,
        "page_obj": page_obj,}

    return render(request, "irina_app/templates/news_list.html", context)


def news_detail_page(request, news_id):
    news_item = get_object_or_404(News, id=news_id)  
    context = {
        "news_item": news_item,
        "news_images": news_item.images.all(),
        "title": news_item.title
        }
    return render(request, "irina_app/templates/news.html", context)

def news_detail_api(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    data = {
        "id": news_item.id,
        "title": news_item.title,
        "text": news_item.text,
        "publish_date": news_item.publish_date.isoformat() if news_item.publish_date else None,
        "images": [
            {'id': img.id, 'image_url': request.build_absolute_uri(img.image.url)} for img in news_item.images.all()
        ]
    }
    return JsonResponse(data)

def starts(request):
    all_starts = Starts.objects.all()
    print("Все соревнования:", all_starts)
    print("Количество:", all_starts.count())
    
    # Пагинация
    page_number = request.GET.get('page_number')
    paginator = Paginator(all_starts, 10)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "irina_app/templates/starts.html", {'page_obj': page_obj})



def get_category_items(request, category_id):
    """Возвращает список доступных предметов для категории"""
    category = get_object_or_404(StartsСategory, id=category_id)
    items = category.available_items.values('id', 'name')
    return JsonResponse({'items': list(items)})

def registration_view(request, start_id):
    start = get_object_or_404(Starts, id=start_id)
    
    # Проверяем, открыта ли регистрация
    if not start.is_registration_open():
        messages.error(request, 'Регистрация на это соревнование закрыта')
        return redirect('all_starts')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, start=start)
        
        if form.is_valid():
            # Проверяем, что загружены все файлы для предметов
            category = form.cleaned_data['category']
            available_items = category.available_items.all()
            
            # Создаем или получаем тренера
            trener, created = Treners.objects.get_or_create(
                email=form.cleaned_data['trener_email'],
                defaults={
                    'last_name': form.cleaned_data['trener_last_name'],
                    'first_name': form.cleaned_data['trener_first_name'],
                    'patronymic': form.cleaned_data.get('trener_patronymic', ''),
                    'phone': form.cleaned_data['trener_phone']
                }
            )
            
            # Создаем спортсмена
            sportsmen = Sportsmens.objects.create(
                last_name=form.cleaned_data['sportsmen_last_name'],
                first_name=form.cleaned_data['sportsmen_first_name'],
                year=form.cleaned_data['sportsmen_year'],
                sport_category=form.cleaned_data['sportsmen_category'],
                trener=trener
            )
            
            # Сохраняем каждый предмет с музыкой
            for item in available_items:
                music_file = request.FILES.get(f'music_{item.id}')
                if music_file:
                    StartsDetails.objects.create(
                        starts=start,
                        sportsmam=sportsmen,
                        sport_item=item,
                        item_music=music_file,
                        starts_category=category
                    )
            
            messages.success(request, f'Спортсмен {sportsmen.last_name} {sportsmen.first_name} успешно зарегистрирован!')
            return redirect('all_starts')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = RegistrationForm(start=start)
    
    return render(request, 'irina_app/templates/registration_form.html', {
        'form': form,
        'start': start,
        'title': f'Регистрация на {start.name}'
    })


def info(request):
    try:
        federation_data = FederationInfo.objects.first()
        context = {
            'title': 'О нас',
            'federation_data': federation_data, 
        }
        return render(request, 'irina_app/templates/info.html', context)
    except Exception as e:
        print(f"Ошибка при загрузке данных для страницы 'О нас': {e}")
        return render(request, 'irina_app/templates/info.html', {'title': 'О нас', 'error': 'Не удалось загрузить информацию'})

          

def user_login(request):
    # Если пользователь уже авторизован
    if request.user.is_authenticated:
        # Проверяем, является ли он суперпользователем
        if request.user.is_superuser:
            messages.success(request, f'Добро пожаловать, {request.user.username}!')
            return redirect('admin_panel')  # Перенаправляем в админ-панель
        else:
            messages.warning(request, 'У вас нет доступа к служебному разделу')
            return redirect('all_starts')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                # Если суперпользователь - логиним и перенаправляем
                login(request, user)
                messages.success(request, f'Добро пожаловать в служебный раздел, {username}!')
                return redirect('admin_panel')
            else:
                # Если обычный пользователь
                messages.error(request, 'Доступ запрещен! Только администраторы имеют доступ к этому разделу.')
                return redirect('user_login')
        else:
            # Неверные учетные данные
            messages.error(request, 'Неверное имя пользователя или пароль. Доступ только для администраторов.')
            return redirect('user_login')
    
    return render(request, 'irina_app/templates/login.html')

@login_required
def admin_panel(request):
    # Проверяем, что пользователь - суперпользователь
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице')
        return redirect('all_starts')
    
    return render(request, 'irina_app/templates/admin_panel.html', {
        'user': request.user,
        'title': 'Служебная панель'
    })


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect(index)


def privacy(request):
    return render(request,"irina_app/templates/privacy.html")
