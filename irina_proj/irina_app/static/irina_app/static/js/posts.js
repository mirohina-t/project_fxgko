document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    let currentSlideIndex = 0;
    const intervalTime = 3000; // Интервал смены слайдов в миллисекундах (3 секунды)

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });
    }

    function nextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        showSlide(currentSlideIndex);
    }

    // Показываем первый слайд при загрузке
    showSlide(currentSlideIndex);

    // Автоматическая смена слайдов
    setInterval(nextSlide, intervalTime);
});

document.addEventListener('DOMContentLoaded', function() {
    const socialLinks = document.querySelectorAll('.social-icon');
    
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const platform = this.classList[1]; // vk, telegram, youtube
            console.log(`Клик по соцсети: ${platform}`);
            
            // Здесь можно добавить аналитику
            // Например, отправку события в Google Analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'social_click', {
                    'social_network': platform,
                    'event_callback': function() {
                        // Открыть ссылку после отправки аналитики
                        window.open(this.href, '_blank');
                    }
                });
                e.preventDefault();
            }
        });
    });
});