from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_lambda,
    aws_lambda_destinations
)


class ProcyonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        record_layer = aws_lambda.LayerVersion(self, 'record_layer',
                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                        code=aws_lambda.Code.from_asset('./lambdas/record_layer'),
                                        removal_policy=RemovalPolicy.DESTROY
                                        )

        odds_layer = aws_lambda.LayerVersion(self, 'odds_layer',
                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                        code=aws_lambda.Code.from_asset('./lambdas/odds_layer'),
                                        removal_policy=RemovalPolicy.DESTROY
                                        )

        # stats_lambda = aws_lambda.Function(self, 'data_lambda',
        #                                 runtime=aws_lambda.Runtime.PYTHON_3_8,
        #                                 code=aws_lambda.Code.from_asset('./lambdas/data'),
        #                                 handler='lambda.handler',
        #                                 on_success=aws_lambda_destinations.LambdaDestination(post_lambda)
        #                                 )

        post_lambda = aws_lambda.Function(self, 'post_lambda', 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset('./lambdas/post_lambda'),
                                        handler='lambda.handler',
                                        layers=[record_layer, odds_layer])

