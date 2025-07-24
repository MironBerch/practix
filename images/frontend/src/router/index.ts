import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import SigninPage from '../pages/SigninPage.vue';
import SignupPage from '../pages/SignupPage.vue';
import SettingsPage from '../pages/SettingsPage.vue';
import FilmworkPage from '../pages/FilmworkPage.vue';
import FilmworksPage from '../pages/FilmworksPage.vue';
import PersonsPage from '../pages/PersonsPage.vue';
import BookmarksPage from '../pages/BookmarksPage.vue';
import PersonPage from '../pages/PersonPage.vue';
import GenrePage from '../pages/GenrePage.vue';
import GenresPage from '../pages/GenresPage.vue';

const router = createRouter(
  {
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'main',
            component: MainPage,
        },
        {
            path: '/signin',
            name: 'signin',
            component: SigninPage,
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignupPage,
        },
        {
            path: '/settings',
            name: 'settings',
            component: SettingsPage,
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignupPage,
        },
        {
            path: '/filmworks',
            name: 'filmworks',
            component: FilmworksPage,
        },
        {
            path: '/filmworks/:uuid',
            name: 'filmwork',
            component: FilmworkPage,
            props: true,
        },
        {
            path: '/genres',
            name: 'genres',
            component: GenrePage,
        },
        {
            path: '/genres/:uuid',
            name: 'genre',
            component: GenresPage,
            props: true,
        },
        {
            path: '/persons',
            name: 'persons',
            component: PersonsPage,
        },
        {
            path: '/persons/:uuid',
            name: 'person',
            component: PersonPage,
            props: true,
        },
        {
            path: '/bookmarks',
            name: 'bookmarks',
            component: BookmarksPage,
        },
    ],
  }
);

export default router;
