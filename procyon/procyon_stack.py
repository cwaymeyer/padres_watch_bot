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

        twitter_lambda_role = aws_iam.Role(self, 'lambda_role',
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

        # postseason odds lambda
        postseason_lambda = aws_lambda.Function(self, 'postseason_lambda', 
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset('lambdas/postseason_lambda'),
                                        handler='lambda.handler',
                                        role=twitter_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )

        postseason_lambda_rule = aws_events.Rule(self, 'postseason_lambda_rule', 
                                        schedule=aws_events.Schedule.expression('cron(00 16 ? 4-9 4,7 *)')) # 1200 EST Wed, Sat

        postseason_lambda_rule.add_target(aws_events_targets.LambdaFunction(postseason_lambda))

        # season team stats lambda
        team_stats_lambda = aws_lambda.Function(self, 'team_stats_lambda',
                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                        code=aws_lambda.Code.from_asset('lambdas/team_stats_lambda'),
                                        handler='lambda.handler',
                                        role=twitter_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )

        team_stats_lambda_rule = aws_events.Rule(self, 'team_stats_lambda_rule', 
                                        schedule=aws_events.Schedule.expression('cron(00 16 ? 4-9 5 *)')) # 1200 EST Thu

        team_stats_lambda_rule.add_target(aws_events_targets.LambdaFunction(team_stats_lambda))

        # weekly hitting stats lambda
        weekly_hitting_stats_lambda = aws_lambda.Function(self, 'weekly_hitting_stats_lambda',
                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                        code=aws_lambda.Code.from_asset('lambdas/weekly_team_leaders_lambda'),
                                        handler='hitters_lambda.handler',
                                        role=twitter_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )

        weekly_hitting_stats_lambda_rule = aws_events.Rule(self, 'weekly_hitting_stats_lambda_rule', 
                                        schedule=aws_events.Schedule.expression('cron(30 15 ? 4-9 2 *)')) # 1140 EST Mon

        weekly_hitting_stats_lambda_rule.add_target(aws_events_targets.LambdaFunction(weekly_hitting_stats_lambda))

        # weekly pitching stats lambda
        weekly_pitching_stats_lambda = aws_lambda.Function(self, 'weekly_pitching_stats_lambda',
                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                        code=aws_lambda.Code.from_asset('lambdas/weekly_team_leaders_lambda'),
                                        handler='pitchers_lambda.handler',
                                        role=twitter_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )

        weekly_pitching_stats_lambda_rule = aws_events.Rule(self, 'weekly_pitching_stats_lambda_rule', 
                                        schedule=aws_events.Schedule.expression('cron(50 15 ? 4-9 2 *)')) # 1145 EST Mon

        weekly_pitching_stats_lambda_rule.add_target(aws_events_targets.LambdaFunction(weekly_pitching_stats_lambda))


