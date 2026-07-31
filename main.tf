resource "kubernetes_config_map" "app_config" {
  metadata {
    name = "app-config"
  }

  data = {
    APP_TITLE    = "🚀 Super Ai Enabled Resume Analyzer"
    APP_SUBTITLE = "Terraform + Kubernetes Demo"
  }
}

resource "kubernetes_deployment" "my_k8s_web" {

  metadata {
    name = "my-k8s-web"

    labels = {
      app = "my-k8s-web"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "my-k8s-web"
      }
    }

    template {

      metadata {
        labels = {
          app = "my-k8s-web"
        }
      }

      spec {

        container {

          name              = "my-k8s-web"
          image             = var.image
          image_pull_policy = "Always"

          port {
            container_port = 5000
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }

            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
          }

          env {
            name = "APP_TITLE"

            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.app_config.metadata[0].name
                key  = "APP_TITLE"
              }
            }
          }

          env {
            name = "APP_SUBTITLE"

            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.app_config.metadata[0].name
                key  = "APP_SUBTITLE"
              }
            }
          }

          volume_mount {
            name       = "app-storage"
            mount_path = "/data"
          }

        }

        volume {
          name = "app-storage"

          persistent_volume_claim {
            claim_name = "my-pvc"
          }
        }

      }
    }
  }
}

resource "kubernetes_service" "my_k8s_web_service" {

  metadata {
    name = "my-k8s-web-service"
  }

  spec {

    selector = {
      app = "my-k8s-web"
    }

    port {
      port        = 5000
      target_port = 5000
    }

    type = "NodePort"

  }
}
