from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration,
    RemovalPolicy
)
from constructs import Construct

import os
from dotenv import load_dotenv



class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        load_dotenv()
        
        #backend
        docker_lambda = _lambda.DockerImageFunction(self, "RealFakeJobAnalysisFunction",
                                                    code=_lambda.DockerImageCode.from_image_asset(os.path.join('..', 'backend')),
                                                    timeout=Duration.seconds(30)
                                                    )
        

        #API Gateway
        api = apigateway.LambdaRestApi(self, "RealfakeJobAnalysisAPI",
                                       handler=docker_lambda,
                                       proxy=True,
                                       endpoint_types=[apigateway.EndpointType.REGIONAL],
                                       description="API for RealFakeJobAnalysis")

        #Frontend
        bucket = s3.Bucket(self, "RealfakeJobAnalysisBucket",
                            bucket_name=os.getenv('FE_BUCKET_NAME'),
                            public_read_access=False,
                            removal_policy=RemovalPolicy.DESTROY,
                            auto_delete_objects=True
        )

        oai = cloudfront.OriginAccessIdentity(self, "RealfakeJobAnalysisOAI")

        distribution = cloudfront.Distribution(self, "RealfakeJobAnalysisDistribution",
                                               default_root_object="index.html",
                                               error_responses=[
                                                    cloudfront.ErrorResponse(
                                                         http_status=403,
                                                         ttl=Duration.seconds(0),
                                                         response_http_status=200,
                                                         response_page_path="/index.html"
                                                    ),
                                                    cloudfront.ErrorResponse(
                                                         http_status=404,
                                                         ttl=Duration.seconds(0),
                                                         response_http_status=200,
                                                         response_page_path="/index.html"
                                                    )
                                                  ],
                                                  default_behavior=cloudfront.BehaviorOptions(
                                                      origin=origins.S3BucketOrigin.with_origin_access_identity(bucket, origin_access_identity=oai),
                                                      allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                                                      cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                                                        viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS),
                                                        geo_restriction=cloudfront.GeoRestriction.allowlist('US', 'CA')
                                                  
                                                  )
        

        distribution.add_behavior("/api/*", origins.HttpOrigin(os.getenv('API_GATEWAY_URL'),
                                                               origin_path=os.getenv('API_GATEWAY_ORIGIN_PATH')),
                                    allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                                    cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                                    origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS)

        bucket.grant_read(oai)

        self.api_url = api.url
        self.bucket_name = bucket.bucket_name
        self.distribution_id = distribution.distribution_id