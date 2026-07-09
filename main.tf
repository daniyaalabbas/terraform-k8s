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
