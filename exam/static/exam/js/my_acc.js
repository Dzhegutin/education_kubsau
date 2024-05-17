document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profile-form');
    const saveBtn = document.getElementById('save-profile-btn');

    saveBtn.addEventListener('click', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/update_profile/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Профиль успешно обновлен!');
                // Дополнительные действия после успешного обновления профиля
            } else {
                alert('Ошибка при обновлении профиля.');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
            alert('Произошла ошибка при обновлении профиля.');
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});




document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('avatar-form');
    const input = document.getElementById('avatar-upload');

    input.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('avatar', file);

        fetch('/update_avatar/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Аватар успешно обновлен!');
                // Можно выполнить дополнительные действия после успешного обновления аватара
            } else {
                alert('Ошибка при обновлении аватара.');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
            alert('Произошла ошибка при обновлении аватара.');
        });
    });

    // Функция для получения значения CSRF-токена из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Ищем куки с указанным именем
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
