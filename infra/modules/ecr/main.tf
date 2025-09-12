resource "aws_ecr_repository" "ecr_etl_formula_1" {
    name = "mateus-almeida-us-east-1-etl-formula-1"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}
