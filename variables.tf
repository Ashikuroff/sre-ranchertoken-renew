variable "rancher_url" {
  description = "Rancher server URL"
  type        = string
  sensitive   = true
}

variable "rancher_token" {
  description = "Rancher API token"
  type        = string
  sensitive   = true
}

variable "insecure" {
  description = "Skip TLS verification"
  type        = bool
  default     = false
}

variable "token_name" {
  description = "Name for the token resource"
  type        = string
  default     = "terraform-managed-token"
}

variable "token_description" {
  description = "Description for the token"
  type        = string
  default     = "Managed by Terraform - Auto-renewed"
}

variable "token_ttl" {
  description = "Token time-to-live in milliseconds"
  type        = number
  default     = 86400000  # 24 hours
}
