output "root_path_bucket_s3" {
    description = "Saida do arn do bucket para utilizacao nas politicas"
    value = aws_s3_bucket.bucket_etl_formula_1.arn
}
