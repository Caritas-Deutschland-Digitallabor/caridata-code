terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    sops = {
      source  = "carlpett/sops"
      version = "0.7.0"
    }
  }
}

provider "docker" {
  host     = "ssh://deploy@${local.target_host}:22"
  ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]

  registry_auth {
    address  = var.ci_registry
    username = var.ci_deploy_user
    password = var.ci_deploy_password
  }
}

provider "sops" {}

data "sops_file" "env_vars" {
  source_file = "secrets/${var.ci_environment_name}.enc.yaml"
  input_type  = "yaml"
}

locals {
  target_host = yamldecode(data.sops_file.env_vars.raw).target_host
  caddy_hosts = yamldecode(data.sops_file.env_vars.raw).caddy_hosts
  basic_auth  = yamldecode(data.sops_file.env_vars.raw).basic_auth
  api_env     = yamldecode(data.sops_file.env_vars.raw).api_env
}

resource "docker_network" "network" {
  name = "${var.ci_environment_name}_caridata_network"
}

resource "docker_image" "frontend" {
  name = var.docker_image_frontend
}

resource "docker_container" "frontend" {
  image   = docker_image.frontend.image_id
  name    = "${var.ci_environment_name}_caridata_frontend"
  restart = "unless-stopped"

  ports {
    internal = 80
  }
}

resource "docker_image" "api" {
  name = var.docker_image_api
}

resource "docker_container" "db_migrations" {
  image   = docker_image.api.image_id
  name    = "${var.ci_environment_name}_caridata_db_migrations"
  restart = "no"
  rm      = true
  command = [
    "alembic",
    "upgrade",
    "head"
  ]
  env = concat(
    [for k, v in local.api_env : format("%s=%s", k, v)],
  )
}

resource "docker_container" "api" {
  image   = docker_image.api.image_id
  name    = "${var.ci_environment_name}_caridata_api"
  restart = "unless-stopped"
  command = [
    "gunicorn",
    "api:app",
    "--workers=2",
    "--worker-class=uvicorn.workers.UvicornWorker",
    "--bind=0.0.0.0:8000",
    "--access-logfile",
    "-",
  ]

  env = concat(
    [for k, v in local.api_env : format("%s=%s", k, v)],
  )
  ports {
    internal = 8000
  }
  networks_advanced {
    name    = docker_network.network.name
    aliases = ["_caridata_api"]
  }
}

resource "local_file" "caddyfile" {
  content = templatefile("./Caddyfile.tftpl", {
    hosts                = local.caddy_hosts,
    docker_port_frontend = docker_container.frontend.ports[0].external,
    docker_port_api      = docker_container.api.ports[0].external,
    basic_auth           = local.basic_auth
  })
  filename = "./Caddyfile"
}

resource "null_resource" "caddyfile_template" {
  triggers = {
    "host_changed"         = local.target_host
    "docker_port_frontend" = docker_container.frontend.ports[0].external
    "docker_port_api"      = docker_container.api.ports[0].external
  }

  provisioner "file" {
    source      = local_file.caddyfile.filename
    destination = "/etc/caddy/caddy.d/${local.target_host}.conf"
  }

  provisioner "remote-exec" {
    inline = ["sudo systemctl reload caddy"]
  }

  connection {
    type = "ssh"
    user = "deploy"
    host = local.target_host
  }
}
