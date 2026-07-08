output "frontend_bucket_name" {
  value       = aws_s3_bucket.frontend_bucket.bucket
  description = "Name of the S3 bucket hosting the frontend"
}

output "cloudfront_domain_name" {
  value       = aws_cloudfront_distribution.frontend_cdn.domain_name
  description = "CloudFront distribution domain"
}

output "frontend_domain" {
  value       = var.domain_name
  description = "Public domain for the frontend"
}