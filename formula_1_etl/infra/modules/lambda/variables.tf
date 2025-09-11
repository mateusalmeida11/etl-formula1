variable "lambda_layer_name" {
    description = "Nome da Camada do ETL"
    type = string

}

variable "lambda_execution_role_arn" {
    description = "ARN da Role que Sera Anexada a Lambda"
    type = string
}

variable "ecr_repository_url" {
    description = "URL do repositorio no ECR"
    type = string
}

variable "image_tag" {
    description = "TAG da imagem passada dinamicamente"
    type = string
}

variable "command_aws_lambda" {
    description = "Path onde o lambda_handler sera executado"
    type = string
}
