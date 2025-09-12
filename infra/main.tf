module "ecr" {
    source = "./modules/ecr"
}

module "s3" {
    source = "./modules/s3"
}

module "iam" {
    source = "./modules/iam"
    bucket_s3_etl_arn = module.s3.root_path_bucket_s3
    aws_lambda_arn= module.lambda.aws_lambda_arn
    layer_name = var.layer_name
}

module "lambda" {
    source = "./modules/lambda"
    url_repos_etl_marketing=module.ecr.ecr_repository_url
    image_tag = var.image_tag
    arn_policy_lambda_execution = module.iam.lambda_execution_role_arn
    command_aws_lambda = var.command_aws_lambda
    lambda_layer_name = var.lambda_layer_name
    depends_on = [module.ecr]

}
