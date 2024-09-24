variable "ssh_key" {
  type      = string
  sensitive = true
}

variable "ci_registry" {
  type      = string
  sensitive = true
}

variable "ci_deploy_user" {
  type      = string
  sensitive = true
}

variable "ci_deploy_password" {
  type      = string
  sensitive = true
}

variable "ci_environment_name" {
  type = string
}

variable "docker_image_frontend" {
  type = string
}

variable "docker_image_api" {
  type = string
}
