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


# SMTP
variable "smtp_server" {
  type        = string
}

variable "smtp_port" {
  type        = string
}

variable "smtp_username" {
  type        = string
}

variable "smtp_password" {
  type        = string
}


# RabbitMQ
variable "rabbitmq_default_user" {
  type        = string
}

variable "rabbitmq_default_pass" {
  type        = string
}


# Notifications DB
variable "notifications_db_user" {
  type        = string
}

variable "notifications_db_password" {
  type        = string
}
