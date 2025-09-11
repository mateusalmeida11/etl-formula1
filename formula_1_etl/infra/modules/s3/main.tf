resource "aws_s3_bucket" "bucket_etl_formula_1" {
    bucket = "mateus-us-east-1-layers-etl-formula-1"
}

resource "aws_s3_bucket_public_access_block" "bucket_etl_formula_1_access_block" {
    bucket = aws_s3_bucket.bucket_etl_formula_1.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}
