resource "aws_lambda_function" "lambda_etl" {
    function_name = var.lambda_layer_name
    role = var.lambda_execution_role_arn
    package_type = "Image"
    image_uri = "${var.ecr_repository_url}:${var.image_tag}"

    image_config {
        command = [var.command_aws_lambda]
    }

    memory_size = 2048
    timeout = 360

    logging_config {
        log_format = "JSON"
    }
}
