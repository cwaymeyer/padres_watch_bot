from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    Duration,
    aws_lambda,
    aws_events,
    aws_events_targets
)


class ProcyonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_layer = aws_lambda.LayerVersion(self, 'lambda_layer',
                                        compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_9],
                                        code=aws_lambda.Code.from_asset('layers'),
                                        removal_policy=RemovalPolicy.DESTROY
                                        )

        post_lambda = aws_lambda.Function(self, 'post_lambda', 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset('lambdas/post_lambda'),
                                        handler='lambda.handler',
                                        timeout=Duration.seconds(60),
                                        layers=[lambda_layer]
                                        )

        post_rule = aws_events.Rule(self, 'post_rule', 
                                        schedule=aws_events.Schedule.expression('cron(*/2 * * * ? *)'))

        post_rule.add_target(aws_events_targets.LambdaFunction(post_lambda))