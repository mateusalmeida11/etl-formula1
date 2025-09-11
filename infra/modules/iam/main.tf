# ----------- 1. Role para Lambda ----------------

resource "aws_iam_role" "lambda_role" {
    name = var.labmda_role_name

    assume_role_policy = jsonencode({
        Version="2012-10-07"
        Statement = [
            {
                Action = "sts.AssumeRole",
                Effect = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "attach_basic_lambda_execution" {
    role = aws_iam_role.lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "policy_access_lambda_s3" {
    name = var.name_iam_policy_access_s3

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3":DeleteObject
                ]
                Effect = "Allow"
                Resource = "${var.bucket_s3_etl_arn}/${var.layer_name}/*"
            }
        ]
    })
}

resource "aws_iam_role_policy" "attach_permission_s3_acess" {
    role = aws_iam_role.lambda_role.name
    policy_arn = aws_iam_policy.policy_access_lambda_s3.arn
}
