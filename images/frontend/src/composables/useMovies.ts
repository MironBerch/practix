import { ref } from 'vue';
import type { Filmwork, FilmworkCollection, Genre, GenreCollection, Person, PersonCollection } from '../types/types';

const BASE_MOVIES_API_URL = import.meta.env.VITE_MOVIES_API_URL;
const API_URL = BASE_MOVIES_API_URL + '/movies/api/v1';

export const useMovies = () => {
    const loading = ref(false);
    const error = ref<string | null>(null);

    const getFilmwork = async (uuid: string): Promise<Filmwork | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/filmworks/${uuid}`);

            if (!response.ok) {
                throw new Error('Filmworks not found');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getFilmworks = async (sort_by: string | null, page_number: number, page_size: number): Promise<FilmworkCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/filmworks`);

            if (!response.ok) {
                throw new Error('Failed to fetch filmworks');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const searchFilmworks = async (query: string, page_number: number, page_size: number): Promise<FilmworkCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/filmworks/search`);

            if (!response.ok) {
                throw new Error('Failed to fetch filmworks');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getGenre = async (uuid: string): Promise<Genre | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/genres/${uuid}`);

            if (!response.ok) {
                throw new Error('Genre not found');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getGenres = async (): Promise<GenreCollection[] | null> => {
        try { 
            loading.value = true;
            const response = await fetch(`${API_URL}/genres`);

            if (!response.ok) {
                throw new Error('Failed to fetch genres');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getPerson = async (uuid: string): Promise<Person | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/persons/${uuid}`);

            if (!response.ok) {
                throw new Error('Person not found');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getPersons = async (page_number: number, page_size: number): Promise<PersonCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/persons`);

            if (!response.ok) {
                throw new Error('Failed to fetch persons');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const getFilmworksByPerson = async (uuid: string): Promise<FilmworkCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/persons/${uuid}/filmworks`);

            if (!response.ok) {
                throw new Error('Failed to fetch filmworks');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const searchPersons = async (query: string, page_number: number, page_size: number): Promise<PersonCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/persons/search`);

            if (!response.ok) {
                throw new Error('Failed to fetch persons');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    };

    return {
        loading,
        error,
        getFilmwork,
        getFilmworks,
        searchFilmworks,
        getGenre,
        getGenres,
        getPerson,
        getPersons,
        searchPersons,
        getFilmworksByPerson,
    };
};
