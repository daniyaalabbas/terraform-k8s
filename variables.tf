variable "replicas" {
  description = "Number of Pods"
  type        = number
  default     = 3
}

variable "image" {
  description = "Docker Image"
  type        = string
  default     = "daniyaalabbas/my-k8s-web:latest"
}
