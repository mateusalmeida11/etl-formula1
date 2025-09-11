output "lambda_execution_role_arn" {
    description = "ARN do iam que sera anexado a lambda"
    value = aws_iam_role.lambda_role.arn
}
