output "aws_lambda_arn" {
    description = "Arn da AWS Lambda"
    value = aws_lambda_function.lambda_etl.arn
}
