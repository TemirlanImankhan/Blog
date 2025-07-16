document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input'); // Поле поиска
    const filterBox = document.getElementById('filter-box'); // Блок фильтрации

    if (searchInput && filterBox) {
        // Показать фильтры при фокусе на поле поиска
        searchInput.addEventListener('focus', () => {
            filterBox.classList.remove('hidden'); // Убираем класс hidden
        });

        // Скрыть фильтры только при клике вне блока фильтрации
        document.addEventListener('click', (event) => {
            if (!filterBox.contains(event.target) && event.target !== searchInput) {
                filterBox.classList.add('hidden'); // Добавляем класс hidden
            }
        });

        // Отключить закрытие при взаимодействии с выпадающим списком
        const categorySelect = document.getElementById('category');
        if (categorySelect) {
            categorySelect.addEventListener('click', (event) => {
                event.stopPropagation(); // Останавливаем всплытие события
            });
        }
    } else {
        console.error('Элементы для фильтрации не найдены.');
    }
});