<template>
    <div class="person-page" v-if="person">
        <!-- Хлебные крошки -->
        <nav class="breadcrumb">
            <router-link to="/persons">Персоны</router-link>
            <span class="separator">/</span>
            <span>{{ person.name }}</span>
        </nav>

        <!-- Основная информация -->
        <div class="person-header">
            <div class="person-avatar-large">
                <div class="avatar-placeholder">{{ getInitials(person.name) }}</div>
            </div>
            <div class="person-info-main">
                <h1 class="person-name">{{ person.name }}</h1>
                <div class="person-roles">
                    <span
                        v-for="role in person.roles"
                        :key="role"
                        :class="['role-tag', getRoleClass(role)]"
                    >
                        {{ getRoleDisplayName(role) }}
                    </span>
                </div>
                <div class="filmworks-count">
                    Участвовал(а) в {{ person.filmwork_ids?.length || 0 }} фильмах
                </div>
            </div>
        </div>

        <!-- Фильмы персоны -->
        <div class="filmworks-section">
            <h2>Фильмы</h2>
            <div v-if="filmworksLoading" class="loading-state">
                <p>Загрузка фильмов...</p>
            </div>
            <div v-else-if="personFilmworks.length > 0" class="filmworks-grid">
                <router-link
                    v-for="filmwork in personFilmworks"
                    :key="filmwork.uuid"
                    :to="`/filmworks/${filmwork.uuid}`"
                    class="filmwork-card"
                >
                    <div class="filmwork-poster">
                        <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
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
                        </div>
                    </div>
                </router-link>
            </div>
            <div v-else class="empty-state">
                <p>Нет информации о фильмах</p>
            </div>
        </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-else-if="loading" class="loading-state">
        <p>Загрузка информации о персоне...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-else-if="error" class="error-state">
        <p>Ошибка: {{ error }}</p>
        <button @click="loadPersonData" class="retry-button">Попробовать снова</button>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, computed } from 'vue'
    import { useRoute } from 'vue-router'
    import { useMovies } from '../composables/useMovies'
    import type { Person, BaseFilmwork } from '../types/types'

    const route = useRoute()
    const { getPerson, getFilmworksByPerson, loading, error } = useMovies()

    // Реактивные данные
    const person = ref<Person | null>(null)
    const personFilmworks = ref<BaseFilmwork[]>([])
    const filmworksLoading = ref(false)

    // Получение UUID из параметров маршрута
    const personUuid = computed(() => route.params.uuid as string)

    // Загрузка данных о персоне
    const loadPersonData = async () => {
        const personData = await getPerson(personUuid.value)
        if (personData) {
            person.value = personData
            await loadPersonFilmworks()
        }
    }

    // Загрузка фильмов персоны
    const loadPersonFilmworks = async () => {
        filmworksLoading.value = true
        try {
            const filmworksData = await getFilmworksByPerson(personUuid.value)
            if (filmworksData && Array.isArray(filmworksData)) {
                personFilmworks.value = filmworksData.flat() as BaseFilmwork[]
            } else {
                personFilmworks.value = []
            }
        } catch (err) {
            console.error('Error loading person filmworks:', err)
            personFilmworks.value = []
        } finally {
            filmworksLoading.value = false
        }
    }

    // Вспомогательные функции
    const getInitials = (name: string) => {
        return name.split(' ')
            .map(part => part.charAt(0))
            .join('')
            .toUpperCase()
            .slice(0, 2)
    }

    const getRoleClass = (role: string) => {
        const roleLower = role.toLowerCase()
        if (roleLower.includes('actor') || roleLower.includes('актер')) {
            return 'role-actor'
        } else if (roleLower.includes('director') || roleLower.includes('режиссер')) {
            return 'role-director'
        } else if (roleLower.includes('writer') || roleLower.includes('сценарист')) {
            return 'role-writer'
        } else if (roleLower.includes('producer') || roleLower.includes('продюсер')) {
            return 'role-producer'
        }
        return 'role-other'
    }

    const getRoleDisplayName = (role: string) => {
        const roleLower = role.toLowerCase()
        if (roleLower.includes('actor') || roleLower.includes('актер')) {
            return 'Актер'
        } else if (roleLower.includes('director') || roleLower.includes('режиссер')) {
            return 'Режиссер'
        } else if (roleLower.includes('writer') || roleLower.includes('сценарист')) {
            return 'Сценарист'
        } else if (roleLower.includes('producer') || roleLower.includes('продюсер')) {
            return 'Продюсер'
        }
        return role
    }

    // Загрузка при монтировании
    onMounted(() => {
        loadPersonData()
    })
</script>

<style scoped>
    .person-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    .breadcrumb {
        margin-bottom: 20px;
        font-size: 14px;
        color: #666;
    }

    .breadcrumb a {
        color: #3498db;
        text-decoration: none;
    }

    .breadcrumb a:hover {
        text-decoration: underline;
    }

    .separator {
        margin: 0 8px;
    }

    .person-header {
        display: flex;
        gap: 30px;
        margin-bottom: 40px;
        align-items: flex-start;
    }

    .person-avatar-large {
        flex-shrink: 0;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .avatar-placeholder {
        font-size: 36px;
        color: white;
        font-weight: bold;
    }

    .person-info-main {
        flex: 1;
    }

    .person-name {
        margin: 0 0 15px 0;
        color: #333;
        font-size: 2.2em;
    }

    .person-roles {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }

    .role-tag {
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 0.85em;
        font-weight: 500;
    }

    .role-actor {
        background: #e3f2fd;
        color: #1976d2;
    }

    .role-director {
        background: #f3e5f5;
        color: #7b1fa2;
    }

    .role-writer {
        background: #e8f5e8;
        color: #388e3c;
    }

    .role-producer {
        background: #fff3e0;
        color: #f57c00;
    }

    .role-other {
        background: #f5f5f5;
        color: #666;
    }

    .filmworks-count {
        font-size: 1.1em;
        color: #666;
        font-weight: 500;
    }

    .filmworks-section {
        margin-top: 40px;
    }

    .filmworks-section h2 {
        margin: 0 0 20px 0;
        color: #333;
        font-size: 1.8em;
    }

    .filmworks-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
    }

    .filmwork-card {
        display: block;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
        background: white;
        cursor: pointer;
    }

    .filmwork-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-decoration: none;
        color: inherit;
    }

    .filmwork-poster {
        width: 100%;
        height: 150px;
        background: #f5f5f5;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }

    .poster-placeholder {
        font-size: 36px;
        color: #ccc;
        font-weight: bold;
    }

    .filmwork-info {
        text-align: center;
    }

    .filmwork-title {
        margin: 0 0 8px 0;
        font-size: 1em;
        font-weight: 600;
        color: #333;
        line-height: 1.3;
    }

    .filmwork-rating {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        margin-bottom: 8px;
        font-size: 0.9em;
    }

    .rating-star {
        font-size: 1em;
    }

    .rating-value {
        font-weight: 600;
        color: #f39c12;
    }

    .filmwork-genres {
        display: flex;
        justify-content: center;
        gap: 4px;
        flex-wrap: wrap;
    }

    .genre-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.7em;
    }

    .loading-state,
    .error-state,
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #666;
    }

    .error-state {
        color: #e74c3c;
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
        .person-header {
            flex-direction: column;
            text-align: center;
            gap: 20px;
        }

        .person-avatar-large {
            align-self: center;
        }

        .person-name {
            font-size: 1.8em;
        }

        .filmworks-grid {
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }
    }

    @media (max-width: 480px) {
        .person-page {
            padding: 15px;
        }

        .filmworks-grid {
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        }

        .filmwork-card {
            padding: 12px;
        }

        .filmwork-poster {
            height: 120px;
        }

        .poster-placeholder {
            font-size: 28px;
        }
    }
</style>
