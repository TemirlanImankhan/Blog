function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

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

function likePost(postId) {
    const likesCountElement = document.getElementById(`likes-count-${postId}`);
    const dislikesCountElement = document.getElementById(`dislikes-count-${postId}`);
    let likesCount = parseInt(likesCountElement.textContent, 10);
    let dislikesCount = parseInt(dislikesCountElement.textContent, 10);

    // Эмуляция обновления на клиенте
    axios.post(`/like/${postId}/`, {}, {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        likesCountElement.textContent = response.data.likes_count;
        dislikesCountElement.textContent = response.data.dislikes_count;
    })
    .catch(error => {
        console.error('Ошибка при запросе:', error);
        // Локальное обновление
        likesCount += 1;
        dislikesCount -= 1;
        document.getElementById(`likes-count-${postId}`).textContent = likesCount;
        document.getElementById(`dislikes-count-${postId}`).textContent = dislikesCount;
    });
}

function dislikePost(postId) {
    const likesCountElement = document.getElementById(`likes-count-${postId}`);
    const dislikesCountElement = document.getElementById(`dislikes-count-${postId}`);
    let likesCount = parseInt(likesCountElement.textContent, 10);
    let dislikesCount = parseInt(dislikesCountElement.textContent, 10);

    // Эмуляция обновления на клиенте
    axios.post(`/dislike/${postId}/`, {}, {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        likesCountElement.textContent = response.data.likes_count;
        dislikesCountElement.textContent = response.data.dislikes_count;
    })
    .catch(error => {
        console.error('Ошибка при дизлайке:', error);
        // Обновление на клиенте, если сервер не работает
        dislikesCount += 1;
        if (likesCount > 0) likesCount -= 1;
        document.getElementById(`likes-count-${postId}`).textContent = likesCount;
        document.getElementById(`dislikes-count-${postId}`).textContent = dislikesCount;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-button');
    const dislikeButtons = document.querySelectorAll('.dislike-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            const postId = button.dataset.postId;

            try {
                const response = await fetch(`/like/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById(`likes-count-${postId}`).textContent = data.likes_count;
                    document.getElementById(`dislikes-count-${postId}`).textContent = data.dislikes_count;
                } else {
                    console.error('Ошибка при отправке запроса на лайк.');
                }
            } catch (error) {
                console.error('Ошибка:', error);
            }
        });
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            const postId = button.dataset.postId;

            try {
                const response = await fetch(`/dislike/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById(`likes-count-${postId}`).textContent = data.likes_count;
                    document.getElementById(`dislikes-count-${postId}`).textContent = data.dislikes_count;
                } else {
                    console.error('Ошибка при отправке запроса на дизлайк.');
                }
            } catch (error) {
                console.error('Ошибка:', error);
            }
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