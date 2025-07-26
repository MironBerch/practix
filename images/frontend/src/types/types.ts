// Common interfaces
export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface ValidationError {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

// Movies API v1 interfaces
export interface HealthCheckResponse {
  status: string;
}

export interface BaseFilmwork {
  uuid: string;
  title: string;
  rating: number;
}

export interface BasePerson {
  uuid: string;
  name: string;
}

export interface Filmwork extends BaseFilmwork {
  description: string;
  genres: string[];
  actors: BasePerson[];
  writers: BasePerson[];
  directors: BasePerson[];
}

export interface Genre {
  uuid: string;
  name: string;
  description: string;
}

export interface Person {
  uuid: string;
  name: string;
  roles: string[];
  filmwork_ids: string[];
}

// Auth API v1 interfaces
export interface ChangeEmailRequest {
  email: string;
}

export interface Confirm2StepVerificationRequest {
  code: string;
}

export interface Confirm2StepVerificationResponse {
  access_token: string;
  refresh_token: string;
}

export interface ErrorResponse {
  message: string;
}

export interface ResendEmailResponse {
  message: string;
}

export interface SignInRequest {
  email: string;
  password: string;
}

export interface SignInResponse {
  message: string;
  temp_token: string;
}

export interface SignUpRequest {
  email: string;
  password: string;
}

export interface UserSession {
  date: string;
  user_agent: string;
  user_device_type: string;
  user_id: string;
}

// UGC API v1 interfaces
export interface FilmworkBookmark {
  filmwork_id: string;
}

export interface Rating {
  average_rating: number | null;
}

export interface Review {
  id: string;
  author_id: string;
  filmwork_id: string;
  text: string;
  pub_date: string;
}

export interface ReviewRating {
  likes: number;
  dislikes: number;
  likes_sum: number;
}

export interface ReviewScore {
  score: 1 | 10;
}

export interface Score {
  score: number;
}

export interface Text {
  text: string;
}

// Collection interfaces
export interface FilmworkCollection extends Array<BaseFilmwork> {}
export interface GenreCollection extends Array<Genre> {}
export interface PersonCollection extends Array<Person> {}
export interface ReviewCollection extends Array<Review> {}
export interface UserSessionCollection extends Array<UserSession> {}

// Query parameter interfaces
export interface PaginationParams {
  page?: {
    number?: number;
    size?: number;
  };
}

export interface FilmworksQueryParams extends PaginationParams {
  sort_by?: string;
  filter?: {
    genres?: string[];
  };
}

export interface SearchQueryParams extends PaginationParams {
  query?: string;
}

// Security
export interface SecurityHTTPBearer {
  HTTPBearer: string[];
}
