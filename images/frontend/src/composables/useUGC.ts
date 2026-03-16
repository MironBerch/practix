import { ref } from "vue";
import type {
  FilmworkBookmark,
  FilmworkBookmarkCollection,
  Score,
  Rating,
  ReviewCollection,
  Review,
  ReviewRating,
  Text,
  ReviewScore,
} from "../types/types";

const BASE_UGC_API_URL = import.meta.env.VITE_UGC_API_URL;
const API_URL = BASE_UGC_API_URL + "/ugc/api/v1";

export const useUGC = () => {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const addFilmworkToBookmarks = async (
    id: string,
    access_token: string,
  ): Promise<FilmworkBookmark | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/bookmarks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed add filmworks to bookmarks");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const removeFilmworkFromBookmarks = async (
    id: string,
    access_token: string,
  ): Promise<FilmworkBookmark | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/bookmarks`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed delete filmworks from bookmarks");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getBookmarks = async (
    access_token: string,
  ): Promise<FilmworkBookmarkCollection[] | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/bookmarks`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch filmworks from bookmarks");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getFilmworkRating = async (id: string): Promise<Rating | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/ratings`);

      if (!response.ok) {
        throw new Error("Failed get filmwork rating");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const addFilmworkRating = async (
    id: string,
    access_token: string,
    data: Score,
  ): Promise<Rating | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/ratings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed add filmworks rating");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const deleteFilmworkRating = async (
    id: string,
    access_token: string,
  ): Promise<Rating | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/bookmarks`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed delete filmworks to bookmarks");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getFilmworkReviews = async (
    id: string,
  ): Promise<ReviewCollection | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/reviews`);

      if (!response.ok) {
        throw new Error("Failed get filmwork reviews");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const addFilmworkReview = async (
    id: string,
    access_token: string,
    data: Text,
  ): Promise<Review | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/filmworks/${id}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed add filmworks review");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const deleteFilmworkReview = async (
    id: string,
    review_id: string,
    access_token: string,
  ): Promise<null> => {
    try {
      loading.value = true;
      const response = await fetch(
        `${API_URL}/filmworks/${id}/reviews/${review_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${access_token}`,
          },
        },
      );

      if (!response.ok) {
        throw new Error("Failed delete filmworks review");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getFilmworkReviewRating = async (
    id: string,
    review_id: string,
  ): Promise<ReviewRating | null> => {
    try {
      loading.value = true;
      const response = await fetch(
        `${API_URL}/filmworks/${id}/reviews/${review_id}/ratings`,
      );

      if (!response.ok) {
        throw new Error("Failed delete filmwork review rating");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const addFilmworkReviewRating = async (
    id: string,
    access_token: string,
    data: ReviewScore,
    review_id: string,
  ): Promise<ReviewRating | null> => {
    try {
      loading.value = true;
      const response = await fetch(
        `${API_URL}/filmworks/${id}/reviews/${review_id}/ratings`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${access_token}`,
          },
          body: JSON.stringify(data),
        },
      );

      if (!response.ok) {
        throw new Error("Failed add filmwork review rating");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const deleteFilmworkReviewRating = async (
    id: string,
    access_token: string,
    review_id: string,
  ): Promise<ReviewRating | null> => {
    try {
      loading.value = true;
      const response = await fetch(
        `${API_URL}/filmworks/${id}/reviews/${review_id}/ratings`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      );

      if (!response.ok) {
        throw new Error("Failed delete filmwork review rating");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    getBookmarks,
    addFilmworkToBookmarks,
    removeFilmworkFromBookmarks,
    getFilmworkRating,
    addFilmworkRating,
    deleteFilmworkRating,
    getFilmworkReviews,
    addFilmworkReview,
    deleteFilmworkReview,
    getFilmworkReviewRating,
    addFilmworkReviewRating,
    deleteFilmworkReviewRating,
  };
};
