Ablauf Action

- Apply:
    - S3 Bucket
    - SSM Parameter Store with Bot Token
    - API Gateway creates URL with Bot Token
    output: API Gatway URL
- API Gateway URL -> SSM Parameter Store
- Upload lambda-code to S3 Bucket
- Apply Lambda Function
- install lambda-code from S3 Bucket
- receive variables from SSM Parameter store