<template>
    <div class="persons-page">
        <!-- Заголовок и управление -->
        <div class="page-header">
            <h1>Актеры и режиссеры</h1>
            <div class="controls">
                <div class="search-control">
                    <input
                        v-model="searchQuery"
                        type="text"
                        placeholder="Поиск по имени..."
                        @input="handleSearch"
                        class="search-input"
                    />
                </div>
                <div class="filter-control">
                    <select v-model="roleFilter" @change="handleFilterChange" class="filter-select">
                        <option value="">Все роли</option>
                        <option value="actor">Актеры</option>
                        <option value="director">Режиссеры</option>
                        <option value="writer">Сценаристы</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Состояние загрузки -->
        <div v-if="loading" class="loading-state">
            <p>Загрузка персон...</p>
        </div>

        <!-- Сообщение об ошибке -->
        <div v-if="error" class="error-state">
            <p>Ошибка: {{ error }}</p>
            <button @click="refreshData" class="retry-button">Попробовать снова</button>
        </div>

        <!-- Результаты поиска -->
        <div v-if="isSearchMode && filteredPersons.length > 0" class="search-info">
            <h2>Результаты поиска для "{{ searchQuery }}"</h2>
            <p>Найдено персон: {{ filteredPersons.length }}</p>
            <button @click="clearSearch" class="clear-search-button">Показать всех</button>
        </div>

        <!-- Список персон -->
        <div v-if="!loading && !error" class="persons-grid">
            <router-link
                v-for="person in filteredPersons"
                :key="person.uuid"
                :to="`/persons/${person.uuid}`"
                class="person-card"
            >
                <div class="person-avatar">
                    <div class="avatar-placeholder">{{ getInitials(person.name) }}</div>
                </div>
                <div class="person-info">
                    <h3 class="person-name">{{ person.name }}</h3>
                    <div class="person-roles">
                        <span
                            v-for="role in person.roles.slice(0, 3)"
                            :key="role"
                            :class="['role-tag', getRoleClass(role)]"
                        >
                            {{ getRoleDisplayName(role) }}
                        </span>
                        <span v-if="person.roles.length > 3" class="role-more">
                            +{{ person.roles.length - 3 }}
                        </span>
                    </div>
                    <div class="person-filmworks">
                        <span class="filmworks-count">
                            Участвовал(а) в {{ person.filmwork_ids?.length || 0 }} фильмах
                        </span>
                    </div>
                </div>
            </router-link>
        </div>

        <!-- Сообщение о пустом состоянии -->
        <div v-if="!loading && !error && filteredPersons.length === 0" class="empty-state">
            <p v-if="isSearchMode">По вашему запросу ничего не найдено</p>
            <p v-else-if="roleFilter">Нет персон с выбранной ролью</p>
            <p v-else>Нет доступных персон</p>
        </div>

        <!-- Пагинация -->
        <div v-if="!loading && !error && filteredPersons.length > 0" class="pagination">
            <button
                :disabled="currentPage === 1"
                @click="previousPage"
                class="pagination-button"
            >
                Назад
            </button>
            <span class="pagination-info">Страница {{ currentPage }}</span>
            <button
                @click="nextPage"
                class="pagination-button"
            >
                Вперед
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, watch, computed } from 'vue'
    import { useMovies } from '../composables/useMovies'
    import type { Person } from '../types/types'

    const {
        loading,
        error,
        getPersons,
        searchPersons
    } = useMovies()

    // Реактивные данные
    const persons = ref<Person[]>([])
    const searchQuery = ref('')
    const roleFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(24)
    const isSearchMode = ref(false)

    // Загрузка данных
    const loadPersons = async () => {
        try {
            let result;
            if (isSearchMode.value && searchQuery.value.trim()) {
                result = await searchPersons(searchQuery.value, currentPage.value, pageSize.value)
            } else {
                result = await getPersons(currentPage.value, pageSize.value)
            }
            
            if (result && Array.isArray(result)) {
                persons.value = result.flat() as Person[]
            } else {
                persons.value = []
            }
        } catch (err) {
            console.error('Error loading persons:', err)
            persons.value = []
        }
    }

    // Отфильтрованные персоны по роли
    const filteredPersons = computed(() => {
        if (!roleFilter.value) {
            return persons.value
        }
        
        return persons.value.filter(person => 
            person.roles?.some(role => 
                role.toLowerCase().includes(roleFilter.value.toLowerCase())
            )
        )
    })

    // Обработчики событий
    const handleSearch = () => {
        isSearchMode.value = searchQuery.value.trim().length > 0
        currentPage.value = 1
        loadPersons()
    }

    const handleFilterChange = () => {
        currentPage.value = 1
        // Фильтрация происходит на клиенте, поэтому не нужно перезагружать данные
    }

    const clearSearch = () => {
        searchQuery.value = ''
        roleFilter.value = ''
        isSearchMode.value = false
        currentPage.value = 1
        loadPersons()
    }

    const previousPage = () => {
        if (currentPage.value > 1) {
            currentPage.value--
            loadPersons()
        }
    }

    const nextPage = () => {
        currentPage.value++
        loadPersons()
    }

    const refreshData = () => {
        loadPersons()
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
        loadPersons()
    })

    // Наблюдатель для пагинации
    watch([currentPage], () => {
        loadPersons()
    })
</script>

<style scoped>
    .persons-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        flex-wrap: wrap;
        gap: 20px;
    }

    .page-header h1 {
        margin: 0;
        color: #333;
        font-size: 2.2em;
    }

    .controls {
        display: flex;
        gap: 15px;
        align-items: center;
    }

    .search-input {
        padding: 10px 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        min-width: 250px;
        font-size: 14px;
    }

    .filter-select {
        padding: 10px 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
        font-size: 14px;
        min-width: 150px;
    }

    .persons-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .person-card {
        display: flex;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
        background: white;
        cursor: pointer;
        gap: 15px;
        align-items: flex-start;
    }

    .person-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        text-decoration: none;
        color: inherit;
    }

    .person-avatar {
        flex-shrink: 0;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .avatar-placeholder {
        font-size: 18px;
        color: white;
        font-weight: bold;
    }

    .person-info {
        flex: 1;
        min-width: 0;
    }

    .person-name {
        margin: 0 0 12px 0;
        font-size: 1.3em;
        font-weight: 600;
        color: #333;
        line-height: 1.2;
    }

    .person-roles {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 10px;
    }

    .role-tag {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75em;
        font-weight: 500;
        white-space: nowrap;
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

    .role-more {
        color: #999;
        font-size: 0.75em;
        align-self: center;
    }

    .person-filmworks {
        margin-top: 8px;
    }

    .filmworks-count {
        font-size: 0.85em;
        color: #666;
    }

    .loading-state,
    .error-state,
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #666;
    }

    .error-state {
        color: #e74c3c;
    }

    .retry-button,
    .clear-search-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .retry-button:hover,
    .clear-search-button:hover {
        background: #2980b9;
    }

    .search-info {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 25px;
        border-left: 4px solid #3498db;
    }

    .search-info h2 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 1.4em;
    }

    .search-info p {
        margin: 0 0 15px 0;
        color: #666;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-top: 40px;
    }

    .pagination-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .pagination-button:hover:not(:disabled) {
        background: #2980b9;
    }

    .pagination-button:disabled {
        background: #bdc3c7;
        cursor: not-allowed;
    }

    .pagination-info {
        font-weight: 600;
        color: #333;
        font-size: 1.1em;
    }

    @media (max-width: 768px) {
        .persons-page {
            padding: 15px;
        }

        .page-header {
            flex-direction: column;
            align-items: stretch;
            text-align: center;
        }

        .page-header h1 {
            font-size: 1.8em;
        }

        .controls {
            flex-direction: column;
            width: 100%;
        }

        .search-input,
        .filter-select {
            min-width: auto;
            width: 100%;
        }

        .persons-grid {
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }

        .person-card {
            padding: 15px;
        }

        .person-avatar {
            width: 50px;
            height: 50px;
        }

        .avatar-placeholder {
            font-size: 16px;
        }

        .person-name {
            font-size: 1.2em;
        }
    }

    @media (max-width: 480px) {
        .persons-grid {
            grid-template-columns: 1fr;
        }

        .person-card {
            flex-direction: column;
            text-align: center;
            gap: 12px;
        }

        .person-avatar {
            align-self: center;
        }

        .search-info {
            padding: 15px;
        }

        .search-info h2 {
            font-size: 1.2em;
        }
    }
</style>