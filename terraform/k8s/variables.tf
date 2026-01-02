variable "token" {
  type        = string
}

variable "cloud_id" {
  type        = string
}

variable "folder_id" {
  type        = string
}


# YC IAM
variable "iam_access_key" {
  type        = string
}

variable "iam_secret_key" {
  type        = string
}


# Container registry id
variable "container_registry_id" {
  type        = string
}


# JWT
variable "jwt_secret_key" {
  type        = string
}

variable "secret_key" {
  type        = string
}


# Django Superuser
variable "django_superuser_username" {
  type        = string
}

variable "django_superuser_email" {
  type        = string
}

variable "django_superuser_password" {
  type        = string
}


# Movies DB
variable "movies_db_user" {
  type        = string
}

variable "movies_db_password" {
  type        = string
}


# Auth DB
variable "auth_db_user" {
  type        = string
}

variable "auth_db_password" {
  type        = string
}
