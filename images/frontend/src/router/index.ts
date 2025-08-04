import { createRouter, createWebHistory } from 'vue-router';
import AuthLayout from '../layouts/AuthLayout.vue';
import MainLayout from '../layouts/MainLayout.vue';

const router = createRouter(
  {
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      // Auth routes
      {
        path: '/auth',
        component: AuthLayout,
        children: [
          {
            path: 'signup',
            name: 'signup',
            component: () => import('../pages/auth/SignupPage.vue')
          },
          {
            path: 'signin',
            name: 'signin',
            component: () => import('../pages/auth/SigninPage.vue')
          },
          {
            path: 'confirm-registration',
            name: 'confirm-registration',
            component: () => import('../pages/auth/ConfirmRegistrationPage.vue')
          },
          {
            path: 'confirm-2fa',
            name: 'confirm-2fa',
            component: () => import('../pages/auth/Confirm2FAPage.vue')
          },
        ]
      },

      // Main app routes (require authentication)
      {
        path: '/',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
          // Main pages
          {
            path: '',
            name: 'main',
            component: () => import('../pages/MainPage.vue')
          },
          {
            path: 'settings',
            name: 'settings',
            component: () => import('../pages/SettingsPage.vue')
          },
          {
            path: 'filmworks',
            name: 'filmworks',
            component: () => import('../pages/FilmworksPage.vue')
          },
          {
            path: 'filmworks/:uuid',
            name: 'filmwork',
            component: () => import('../pages/FilmworkPage.vue'),
            props: true
          },
          {
            path: 'genres',
            name: 'genres',
            component: () => import('../pages/GenresPage.vue')
          },
          {
            path: 'genres/:uuid',
            name: 'genre',
            component: () => import('../pages/GenrePage.vue'),
            props: true
          },
          {
            path: 'persons',
            name: 'persons',
            component: () => import('../pages/PersonsPage.vue')
          },
          {
            path: 'persons/:uuid',
            name: 'person',
            component: () => import('../pages/PersonPage.vue'),
            props: true
          },
          {
            path: 'bookmarks',
            name: 'bookmarks',
            component: () => import('../pages/BookmarksPage.vue')
          },

          // User account routes
          {
            path: 'change-email',
            name: 'change-email',
            component: () => import('../pages/user/ChangeEmailPage.vue')
          },
          {
            path: 'confirm-change-email',
            name: 'confirm-change-email',
            component: () => import('../pages/user/ConfirmChangeEmailPage.vue')
          },
          {
            path: 'change-password',
            name: 'change-password',
            component: () => import('../pages/user/ChangePasswordPage.vue')
          },
          {
            path: 'sessions',
            name: 'sessions',
            component: () => import('../pages/user/SessionsPage.vue')
          }
        ]
      }
    ]
  }
);

// Navigation guard for authentication
router.beforeEach(
  (to, from, next) => {
    const isAuthenticated = /* your auth check logic, e.g.: */ localStorage.getItem('access_token') !== null;
    
    if (to.meta.requiresAuth && !isAuthenticated) {
      next({ name: 'signin' });
    } else if ((to.name === 'signin' || to.name === 'signup') && isAuthenticated) {
      next({ name: 'main' }); // Redirect if user is already authenticated
    } else {
      next();
    }
  }
);

export default router;
