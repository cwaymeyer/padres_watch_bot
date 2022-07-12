from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)


class ProcyonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        post_lambda = aws_lambda.Function(self, "post_lambda", 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        handler="lambda_function.lambda_handler",
                                        code=aws_lambda.Code.from_asset("./src/lambdas/post"))
