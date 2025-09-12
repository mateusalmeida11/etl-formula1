output "ecr_repository_url" {
    description = "URL de saida do repositorio do ECR"
    value = aws_ecr_repository.ecr_etl_formula_1.repository_url
}
