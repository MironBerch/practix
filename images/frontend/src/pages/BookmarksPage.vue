<template>
    <div class="bookmarks-page">
        <!-- Заголовок -->
        <div class="page-header">
            <h1>Мои закладки</h1>
            <p v-if="bookmarksCount > 0">Найдено фильмов: {{ bookmarksCount }}</p>
            <p v-else>У вас пока нет фильмов в закладках</p>
        </div>

        <!-- Состояние загрузки -->
        <div v-if="loading" class="loading-state">
            <p>Загрузка закладок...</p>
        </div>

        <!-- Сообщение об ошибке -->
        <div v-if="error" class="error-state">
            <p>Ошибка: {{ error }}</p>
            <button @click="loadBookmarks" class="retry-button">Попробовать снова</button>
        </div>

        <!-- Сообщение о необходимости авторизации -->
        <div v-if="!isAuthenticated" class="auth-required">
            <h2>Для просмотра закладок необходимо авторизоваться</h2>
            <router-link to="/signin" class="auth-link">Войти в аккаунт</router-link>
        </div>

        <!-- Список фильмов в закладках -->
        <div v-if="isAuthenticated && !loading && !error && bookmarksCount > 0" class="bookmarks-grid">
            <router-link
                v-for="filmwork in bookmarkedFilmworks"
                :key="filmwork.uuid"
                :to="`/filmworks/${filmwork.uuid}`"
                class="filmwork-card"
            >
                <div class="filmwork-poster">
                    <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
                    <div class="bookmark-indicator">★</div>
                </div>
                <div class="filmwork-info">
                    <h3 class="filmwork-title">{{ filmwork.title }}</h3>
                    <div class="filmwork-rating">
                        <span class="rating-star">⭐</span>
                        <span class="rating-value">{{ filmwork.rating?.toFixed(1) || '0.0' }}</span>
                    </div>
                    <div v-if="filmwork.genres && filmwork.genres.length > 0" class="filmwork-genres">
                        <span
                            v-for="genre in filmwork.genres.slice(0, 2)"
                            :key="genre"
                            class="genre-tag"
                        >
                            {{ genre }}
                        </span>
                        <span v-if="filmwork.genres.length > 2" class="genre-more">
                            +{{ filmwork.genres.length - 2 }}
                        </span>
                    </div>
                    <button 
                        @click.prevent="removeFromBookmarks(filmwork.uuid)"
                        class="remove-bookmark-btn"
                    >
                        Удалить из закладок
                    </button>
                </div>
            </router-link>
        </div>

        <!-- Сообщение о пустых закладках -->
        <div v-if="isAuthenticated && !loading && !error && bookmarksCount === 0" class="empty-bookmarks">
            <div class="empty-state">
                <h2>Закладок пока нет</h2>
                <p>Добавляйте фильмы в закладки, чтобы легко находить их позже</p>
                <router-link to="/filmworks" class="explore-link">Найти фильмы</router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useMovies } from '../composables/useMovies'
    import { useUGC } from '../composables/useUGC'
    import type { BaseFilmwork, FilmworkBookmark } from '../types/types'

    const router = useRouter()
    const { getFilmwork, loading: moviesLoading } = useMovies()
    const { 
        getBookmarks, 
        removeFilmworkFromBookmarks,
        loading: ugcLoading,
        error 
    } = useUGC()

    // Реактивные данные
    const bookmarks = ref<FilmworkBookmark[]>([])
    const bookmarkedFilmworks = ref<BaseFilmwork[]>([])
    const removalLoading = ref<string | null>(null)

    // Проверка аутентификации
    const isAuthenticated = computed(() => {
        return !!localStorage.getItem('access_token')
    })

    // Количество закладок
    const bookmarksCount = computed(() => bookmarkedFilmworks.value.length)

    // Состояние загрузки
    const loading = computed(() => moviesLoading.value || ugcLoading.value)

    // Загрузка закладок
    const loadBookmarks = async () => {
        if (!isAuthenticated.value) return

        const token = localStorage.getItem('access_token')
        if (!token) return

        try {
            const bookmarksData = await getBookmarks(token)
            if (bookmarksData && Array.isArray(bookmarksData)) {
                bookmarks.value = bookmarksData.flat() as FilmworkBookmark[]
                await loadBookmarkedFilmworks()
            } else {
                bookmarks.value = []
                bookmarkedFilmworks.value = []
            }
        } catch (err) {
            console.error('Error loading bookmarks:', err)
            bookmarks.value = []
            bookmarkedFilmworks.value = []
        }
    }

    // Загрузка информации о фильмах в закладках
    const loadBookmarkedFilmworks = async () => {
        bookmarkedFilmworks.value = []
        
        for (const bookmark of bookmarks.value) {
            try {
                const filmwork = await getFilmwork(bookmark.filmwork_id)
                if (filmwork) {
                    bookmarkedFilmworks.value.push(filmwork)
                }
            } catch (err) {
                console.error(`Error loading filmwork ${bookmark.filmwork_id}:`, err)
            }
        }
    }

    // Удаление из закладок
    const removeFromBookmarks = async (filmworkUuid: string) => {
        if (!isAuthenticated.value) return

        const token = localStorage.getItem('access_token')
        if (!token) return

        removalLoading.value = filmworkUuid
        
        try {
            await removeFilmworkFromBookmarks(filmworkUuid, token)
            
            // Удаляем фильм из локального списка
            bookmarkedFilmworks.value = bookmarkedFilmworks.value.filter(
                filmwork => filmwork.uuid !== filmworkUuid
            )
            
            // Обновляем список закладок
            bookmarks.value = bookmarks.value.filter(
                bookmark => bookmark.filmwork_id !== filmworkUuid
            )
        } catch (err) {
            console.error('Error removing bookmark:', err)
        } finally {
            removalLoading.value = null
        }
    }

    // Загрузка при монтировании
    onMounted(() => {
        if (isAuthenticated.value) {
            loadBookmarks()
        }
    })
</script>

<style scoped>
    .bookmarks-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    .page-header {
        text-align: center;
        margin-bottom: 40px;
    }

    .page-header h1 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 2.5em;
    }

    .page-header p {
        margin: 0;
        color: #666;
        font-size: 1.1em;
    }

    .bookmarks-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }

    .filmwork-card {
        display: block;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
        background: white;
        cursor: pointer;
        position: relative;
    }

    .filmwork-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        text-decoration: none;
        color: inherit;
    }

    .filmwork-poster {
        width: 100%;
        height: 220px;
        background: #f5f5f5;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        position: relative;
    }

    .poster-placeholder {
        font-size: 52px;
        color: #ccc;
        font-weight: bold;
    }

    .bookmark-indicator {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #f39c12;
    }

    .filmwork-info {
        text-align: center;
    }

    .filmwork-title {
        margin: 0 0 12px 0;
        font-size: 1.2em;
        font-weight: 600;
        color: #333;
        line-height: 1.3;
    }

    .filmwork-rating {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin-bottom: 12px;
    }

    .rating-star {
        font-size: 1.3em;
    }

    .rating-value {
        font-weight: 600;
        color: #f39c12;
        font-size: 1.1em;
    }

    .filmwork-genres {
        display: flex;
        justify-content: center;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }

    .genre-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.85em;
        font-weight: 500;
    }

    .genre-more {
        color: #666;
        font-size: 0.85em;
        align-self: center;
    }

    .remove-bookmark-btn {
        width: 100%;
        padding: 10px;
        background: #e74c3c;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: background-color 0.2s;
    }

    .remove-bookmark-btn:hover {
        background: #c0392b;
    }

    .remove-bookmark-btn:disabled {
        background: #bdc3c7;
        cursor: not-allowed;
    }

    .loading-state,
    .error-state,
    .auth-required,
    .empty-bookmarks {
        text-align: center;
        padding: 60px 20px;
    }

    .loading-state {
        color: #666;
    }

    .error-state {
        color: #e74c3c;
    }

    .auth-required {
        background: #f8f9fa;
        border-radius: 12px;
        margin: 40px 0;
    }

    .auth-required h2 {
        margin: 0 0 20px 0;
        color: #333;
    }

    .auth-link {
        display: inline-block;
        background: #3498db;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        transition: background-color 0.2s;
    }

    .auth-link:hover {
        background: #2980b9;
        text-decoration: none;
        color: white;
    }

    .empty-state {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 60px 40px;
    }

    .empty-state h2 {
        margin: 0 0 15px 0;
        color: #333;
    }

    .empty-state p {
        margin: 0 0 25px 0;
        color: #666;
        font-size: 1.1em;
    }

    .explore-link {
        display: inline-block;
        background: #27ae60;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        transition: background-color 0.2s;
    }

    .explore-link:hover {
        background: #219a52;
        text-decoration: none;
        color: white;
    }

    .retry-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 15px;
    }

    .retry-button:hover {
        background: #2980b9;
    }

    @media (max-width: 768px) {
        .bookmarks-page {
            padding: 15px;
        }

        .page-header h1 {
            font-size: 2em;
        }

        .bookmarks-grid {
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }

        .filmwork-card {
            padding: 15px;
        }

        .filmwork-poster {
            height: 180px;
        }

        .empty-state {
            padding: 40px 20px;
        }
    }

    @media (max-width: 480px) {
        .bookmarks-grid {
            grid-template-columns: 1fr;
        }
        
        .page-header h1 {
            font-size: 1.8em;
        }
    }
</style>
