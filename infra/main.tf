module "ecr" {
    source = "./modules/ecr"
}

module "s3" {
    source = "./modules/s3"
}

module "iam" {
    source = "./modules/iam"
    bucket_s3_etl_arn = module.s3.root_path_bucket_s3
    layer_name = var.layer_name
}

module "lambda" {
    source = "./modules/lambda"
    ecr_repository_url=module.ecr.ecr_repository_url
    image_tag = var.image_tag
    lambda_execution_role_arn" = module.iam.lambda_execution_role_arn
    command_aws_lambda = var.command_aws_lambda
    lambda_layer_name = var.lambda_layer_name
    depends_on = [module.ecr]

}
