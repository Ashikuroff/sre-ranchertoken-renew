resource "rancher2_token" "this" {
  name        = var.token_name
  description = var.token_description
  ttl         = var.token_ttl
}

output "token_id" {
  description = "The ID of the created token"
  value       = rancher2_token.this.id
  sensitive   = true
}

output "token_key" {
  description = "The token key (only shown on creation)"
  value       = rancher2_token.this.token
  sensitive   = true
}
