variable "lambda_role_name" {
    description = "Nome da Politica de Execucao Basica de Uma Lambda"
    type = string
    default = "lambda_role_basic_execution_iam"
}

variable "name_iam_policy_access_s3" {
    description = "Politica de Permissao ao S3"
    type = string
    default = "lambda_acess_s3_policy"

}

variable "bucket_s3_etl_arn" {
    description = "Arn do Bucket para Anexar Politica"
    type = string
}

variable "layer_name" {
    description = "Nome da Camada que Lambda Ira Executar"
    type = string
}
