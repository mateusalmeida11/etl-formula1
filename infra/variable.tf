variable "image_tag" {
    description = "Tag que sera gerada dinamicamente pelo git"
    type = string
}

variable "command_aws_lambda" {
    description = "Path onde a lambda sera executada"
    type = string
    default = ""

}

variable "lambda_layer_name" {
    description = "Nome da Camada da Lambda"
    type = string
    default=""

}

variable "layer_name" {
    description = "Nome da Camada que Lambda Ira Executar"
    type = string
    default=""
}
