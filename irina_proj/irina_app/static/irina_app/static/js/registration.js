let availableItems = {};
let selectedItems = new Set();

// При выборе категории загружаем доступные предметы
document.getElementById('category-select').addEventListener('change', function() {
    const categoryId = this.value;
    if (categoryId) {
        loadAvailableItems(categoryId);
    } else {
        document.getElementById('items-section').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
    }
});

function loadAvailableItems(categoryId) {
    fetch(`/get-category-items/${categoryId}/`)
        .then(response => response.json())
        .then(data => {
            availableItems = data.items;
            renderItemsForm();
            document.getElementById('items-section').style.display = 'block';
            document.getElementById('submit-btn').style.display = 'block';
        })
        .catch(error => {
            console.error('Ошибка загрузки предметов:', error);
            alert('Ошибка загрузки доступных предметов');
        });
}

function renderItemsForm() {
    const container = document.getElementById('items-container');
    container.innerHTML = '';
    selectedItems.clear();
    
    availableItems.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item-row';
        itemDiv.dataset.itemId = item.id;
        itemDiv.innerHTML = `
            <div class="item-header">
                <strong>${item.name}</strong>
            </div>
            <div class="form-group">
                <label>Музыкальное сопровождение (MP3):</label>
                <input type="file" name="music_${item.id}" class="music-file" accept="audio/*" data-item-id="${item.id}" required>
                <audio class="audio-preview" controls style="display: none; margin-top: 10px;">
                    <source src="" type="audio/mpeg">
                </audio>
            </div>
        `;
        container.appendChild(itemDiv);
        
        // предпросмотр музыки
        const fileInput = itemDiv.querySelector('.music-file');
        const audioPreview = itemDiv.querySelector('.audio-preview');
        
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.includes('audio/mpeg')) {
                const url = URL.createObjectURL(file);
                audioPreview.querySelector('source').src = url;
                audioPreview.load();
                audioPreview.style.display = 'block';
            } else if (file) {
                alert('Пожалуйста, загружайте только MP3 файлы');
                this.value = '';
                audioPreview.style.display = 'none';
            }
        });
    });
}

// Автоматический ресайз textarea (если есть)
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});

// Улучшение touch-событий для мобильных
if ('ontouchstart' in window) {
    document.querySelectorAll('.button-primary, .delete-row-btn, #add-item-btn').forEach(btn => {
        btn.style.cursor = 'pointer';
        btn.addEventListener('touchstart', function(e) {
            this.style.transform = 'scale(0.98)';
        });
        btn.addEventListener('touchend', function(e) {
            this.style.transform = 'scale(1)';
        });
    });
}

// Адаптивная проверка ориентации
window.addEventListener('resize', function() {
    const container = document.querySelector('.registration-container');
    if (window.innerHeight < 600 && window.innerWidth > window.innerHeight) {
        container.style.margin = '5px auto';
    } else {
        container.style.margin = '20px auto';
    }
});