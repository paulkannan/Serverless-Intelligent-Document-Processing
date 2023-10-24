from constructs import Construct
from aws_cdk import (
    Duration,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_event_sources as eventsources,
    aws_apigateway as apigateway,
    aws_rekognition as rekognition,
    aws_s3 as s3,
    Stack,
    App
)

class CdklambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Input Bucket
        self.input_bucket = s3.Bucket(self, 'input-bucket',
                                      versioned=True,
                                      bucket_name='docs-landing-bucket',
                                      encryption=s3.BucketEncryption.S3_MANAGED,
                                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                      enforce_ssl=True)
        
        # Valid Bucket
        self.valid_bucket = s3.Bucket(self, 'valid-bucket',
                                      versioned=True,
                                      bucket_name='valid-docs-bucket',
                                      encryption=s3.BucketEncryption.S3_MANAGED,
                                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                      enforce_ssl=True)
        
        # InValid Bucket
        self.invalid_bucket = s3.Bucket(self, 'invalid-bucket',
                                      versioned=True,
                                      bucket_name='invalid-docs-bucket',
                                      encryption=s3.BucketEncryption.S3_MANAGED,
                                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                      enforce_ssl=True)
        
        # Create Rekognition Collection
        rekognition_collection = rekognition.CfnCollection(self, "RekognitionCollection",collection_id="MyRekognitionCollection")

        # Create a resource policy for the collection
        resource_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "rekognition:*",
                    "Resource": "*"
                }
            ]
        }        

        python_lambda_kwargs = {
            'handler': 's3event.lambda_handler',
            'runtime': lambda_.Runtime.PYTHON_3_9,
            'timeout': Duration.minutes(10),
            'memory_size': 4096
        }
        # Create the Rest API
        rest_api = apigateway.RestApi(
            self, "RestApi",
            endpoint_types=[apigateway.EndpointType.REGIONAL]
        )

        # Trigger Textract Lambda
        trigger_textract = lambda_.Function(self, 'file-upload-trigger', **python_lambda_kwargs,
                                            code=lambda_.Code.from_asset('s3event.zip'),
                                            function_name="start-textract")

        # Lambda Integration
        integration = apigateway.LambdaIntegration(trigger_textract)

        # Create Resource and Method
        resource = rest_api.root.add_resource("upload")
        method = resource.add_method("PUT", integration)     
        
        # Grant full access to S3 and Textract
        trigger_textract.add_to_role_policy(iam.PolicyStatement(
            actions=[
                's3:GetObject',
                's3:PutObject',
                's3:ListBucket',
                's3:DeleteObject',
                'textract:*',
                'comprehend:*',
                'rekognition:*'
            ],
            resources=['*']  # This allows access to all S3 buckets and Textract resources
        ))

        # Add Trigger and Environment Variables
        trigger_textract.add_event_source(eventsources.S3EventSource(self.input_bucket, events=[s3.EventType.OBJECT_CREATED]))
        

app = App()
CdklambdaStack(app, "CdklambdaStack")
app.synth()