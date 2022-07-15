from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_lambda,
    aws_events,
    aws_events_targets
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

        post_lambda = aws_lambda.Function(self, 'post_lambda', 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset('./lambdas/post_lambda'),
                                        handler='lambda.handler',
                                        layers=[record_layer, odds_layer]
                                        )

        post_rule = aws_events.Rule(self, 'post_rule', 
                                        schedule=aws_events.Schedule.cron(
                                            minute='0',
                                            hour='12',
                                            month='*',
                                            week_day='MON, THU',
                                            year='*'
                                        ))

        post_rule.add_target(aws_events_targets.LambdaFunction(post_lambda))
