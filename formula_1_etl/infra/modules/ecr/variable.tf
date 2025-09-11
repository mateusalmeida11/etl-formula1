resoure "aws_ecr_repository" "ecr_etl_formula-1" {
    name = "etl-formula-1",
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}
