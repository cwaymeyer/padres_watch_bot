from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    Duration,
    aws_lambda,
    aws_events,
    aws_events_targets,
    aws_iam
)
import configparser

config = configparser.RawConfigParser()
config.read('config.properties')

AWS_ACCOUNT_ID = config.get('AWS', 'account_id')
AWS_REGION = config.get('AWS', 'region')


class ProcyonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        post_lambda_role = aws_iam.Role(self, 'lambda_role',
                                        assumed_by=aws_iam.ServicePrincipal(service='lambda.amazonaws.com'),
                                        inline_policies={
                                            'LambdaBasicExecutionRole': aws_iam.PolicyDocument(
                                                statements=[
                                                    aws_iam.PolicyStatement(
                                                        actions=[
                                                            'logs:CreateLogGroup',
                                                            'logs:CreateLogStream',
                                                            'logs:PutLogEvents'
                                                        ],
                                                        resources=['*']
                                                    )
                                                ]
                                            ), 
                                            'SecretsManagerPermissions': aws_iam.PolicyDocument(
                                                statements=[
                                                    aws_iam.PolicyStatement(
                                                        actions=[
                                                            'secretsmanager:GetResourcePolicy',
                                                            'secretsmanager:GetSecretValue',
                                                            'secretsmanager:DescribeSecret',
                                                            'secretsmanager:ListSecretVersionIds'
                                                        ],
                                                        resources=[
                                                            'arn:aws:secretsmanager:{}:{}:secret:twitter-api*'.format(AWS_REGION, AWS_ACCOUNT_ID)
                                                        ]
                                                    )
                                                ]
                                            )
                                        }
                                        )   

        lambda_layer = aws_lambda.LayerVersion(self, 'lambda_layer',
                                        compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_9],
                                        code=aws_lambda.Code.from_asset('layers'),
                                        removal_policy=RemovalPolicy.DESTROY
                                        )

        post_lambda = aws_lambda.Function(self, 'post_lambda', 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset('lambdas/post_lambda'),
                                        handler='lambda.handler',
                                        role=post_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )

        post_rule = aws_events.Rule(self, 'post_rule', 
                                        schedule=aws_events.Schedule.expression('cron(30 16 ? 4-9 2,5 *)'))

        post_rule.add_target(aws_events_targets.LambdaFunction(post_lambda))

