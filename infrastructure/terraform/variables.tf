variable "domain_name" {
  description = "Root domain for the frontend"
  type        = string
  default     = "devcosta-solutions.com"
}

variable "hosted_zone_id" {
  description = "Route 53 hosted zone ID for the domain"
  type        = string
  default     = "Z0477722TRPLQX8FVL2D"
}
