import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../layouts/MainLayout.vue";
import { refreshToken } from '../composables/useAuth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Auth routes
    {
      path: "/auth",
      component: MainLayout,
      children: [
        {
          path: "signup",
          name: "signup",
          component: () => import("../pages/auth/SignupPage.vue"),
        },
        {
          path: "signin",
          name: "signin",
          component: () => import("../pages/auth/SigninPage.vue"),
        },
      ],
    },

    // Main app routes (require authentication)
    {
      path: "/",
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        // Main pages
        // Redirect from root to filmworks
        {
          path: "",
          redirect: { name: "filmworks" }
        },
        {
          path: "settings",
          name: "settings",
          component: () => import("../pages/SettingsPage.vue"),
        },
        {
          path: "filmworks",
          name: "filmworks",
          component: () => import("../pages/filmworks/FilmworksPage.vue"),
        },
        {
          path: "filmworks/:id",
          name: "filmwork",
          component: () => import("../pages/filmworks/FilmworkPage.vue"),
          props: true,
        },
        {
          path: "persons",
          name: "persons",
          component: () => import("../pages/persons/PersonsPage.vue"),
        },
        {
          path: "persons/:id",
          name: "person",
          component: () => import("../pages/persons/PersonPage.vue"),
          props: true,
        },
        {
          path: "bookmarks",
          name: "bookmarks",
          component: () => import("../pages/BookmarksPage.vue"),
        },

        // User account routes
        {
          path: "change-email",
          name: "change-email",
          component: () => import("../pages/user/ChangeEmailPage.vue"),
        },
        {
          path: "change-password",
          name: "change-password",
          component: () => import("../pages/user/ChangePasswordPage.vue"),
        },
        {
          path: "sessions",
          name: "sessions",
          component: () => import("../pages/user/SessionsPage.vue"),
        },
      ],
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const accessToken = localStorage.getItem('access_token');

  const isTokenValid = (token: string | null): boolean => {
    if (!token) return false;
    return true;
  };

  if (to.meta.requiresAuth) {
    const refreshed = await refreshToken();
    if (refreshed) {
      next();
    } else {
      next({ name: 'signin' });
    }
  }
  else if ((to.name === 'signin' || to.name === 'signup') && isTokenValid(accessToken)) {
    next({ name: 'filmworks' });
  } else {
    next();
  }
});

export default router;
