document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("news-modal");
    const closeButton = modal.querySelector(".close-button");
    const openModalLinks = document.querySelectorAll(".open-modal-link");

    openModalLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); 
            const newsId = this.getAttribute('data-news-id');
            loadNewsDetails(newsId);
            modal.style.display = "block";
        });
    });  
    
    closeButton.addEventListener('click', function() {
        modal.style.display = "none";
        clearModal();
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            clearModal();
        }
    });
});

function clearModal() {
    document.getElementById("modal-news-gallery").innerHTML = "";
    // document.getElementById("modal-news-text").innerHTML = "";
    document.getElementById("modal-news-title").innerHTML = "";
}

function loadNewsDetails(newsId) {
    fetch(`/api/news/${newsId}/`) 
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("modal-news-title").textContent = data.title || 'Без заголовка';
            // document.getElementById("modal-news-text").innerHTML = data.text || 'Текст отсутствует';
            
            const gallery = document.getElementById("modal-news-gallery");
            gallery.innerHTML = "";
            
            if (data.images && data.images.length > 0) {
                data.images.forEach(imageData => {
                    const img = document.createElement('img');
                    img.src = imageData.image_url;
                    img.alt = `Image ${imageData.id}`;
                    img.style.maxWidth = '100%';
                    img.style.marginBottom = '10px';
                    gallery.appendChild(img);
                });
            } else {
                gallery.innerHTML = '<p>Нет изображений для этой новости</p>';
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке:', error);
            document.getElementById("modal-news-title").textContent = 'Ошибка загрузки';
            // document.getElementById("modal-news-text").innerHTML = 'Не удалось загрузить новость';
        });
}



