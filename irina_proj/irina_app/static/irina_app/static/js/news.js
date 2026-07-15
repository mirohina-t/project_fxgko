document.addEventListener('DOMContentLoaded', function() {
    let buttonToTop = document.getElementById('button_to_top');
    const allButtons = document.querySelectorAll('button');
    allButtons.forEach((btn, idx) => {
    buttonToTop.style.display = 'none'})
    
    // Функция показа/скрытия
    function checkScrollPosition() {
        if (window.scrollY > 300) {
            buttonToTop.style.display = 'flex';
            buttonToTop.style.alignItems = 'center';
            buttonToTop.style.justifyContent = 'center';
            console.log('Показываем кнопку');
        } else {
            buttonToTop.style.display = 'none';
            console.log('Скрываем кнопку');
        }
    }
    
    // Проверяем при прокрутке
    window.addEventListener('scroll', checkScrollPosition);
    
    // Проверяем сразу после загрузки
    checkScrollPosition();
    
    // Клик для прокрутки вверх
    buttonToTop.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('Клик по кнопке, скроллим вверх');
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    });
});

