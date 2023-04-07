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


lambdas = [
    {
        'name': 'weekly_hitting_stats_lambda',
        'folder': 'lambdas/team_leaders_lambda',
        'file': 'weekly_hitters_lambda',
        'cron': ['30 14 ? 4-9 2 *'] # 1030 EST Mon
    },
    {
        'name': 'weekly_pitching_stats_lambda',
        'folder': 'lambdas/team_leaders_lambda',
        'file': 'weekly_pitchers_lambda',
        'cron': ['00 15 ? 4-9 2 *'] # 1100 EST Mon
    },
    {
        'name': 'series_results_lambda',
        'folder': 'lambdas/series_results_lambda',
        'file': 'lambda',
        'cron': ['00 15 ? 4-9 3 *', '30 16 ? 4-9 6 *'] # 11 EST Tue, 1230 EST Fri
    },
    {
        'name': 'postseason_lambda',
        'folder': 'lambdas/postseason_lambda',
        'file': 'lambda',
        'cron': ['30 16 ? 4-9 7 *'] # 1230 EST Sat
    },
    {
        'name': 'team_stats_lambda',
        'folder': 'lambdas/team_stats_lambda',
        'file': 'lambda',
        'cron': ['00 15 ? 4-9 5 *'] # 1100 EST Thu
    },
    {
        'name': 'monthly_hitting_stats_lambda',
        'folder': 'lambdas/team_leaders_lambda',
        'file': 'monthly_hitters_lambda',
        'cron': ['00 19 1 5-10 ? *'] # 1500 EST 1st of month
    },
    {
        'name': 'monthly_pitching_stats_lambda',
        'folder': 'lambdas/team_leaders_lambda',
        'file': 'monthly_pitchers_lambda',
        'cron': ['30 19 1 5-10 ? *'] # 1530 EST 1st of month
    },
    {
        'name': 'war_rankings_lambda',
        'folder': 'lambdas/war_lambda',
        'file': 'lambda',
        'cron': ['00 15 ? 4-9 4 *'] # 1100 EST Wed
    }
]


class ProcyonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role for lambdas
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

        # Lamda layer for dependencies
        lambda_layer = aws_lambda.LayerVersion(self, 'lambda_layer',
                                        compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_9],
                                        code=aws_lambda.Code.from_asset('layers'),
                                        removal_policy=RemovalPolicy.DESTROY
                                        )

        # create Lambdas and Eventbridge cron expressions
        for lamb in lambdas:
            curr_lambda = aws_lambda.Function(self, lamb['name'],
                                        function_name=lamb['name'],
                                        runtime=aws_lambda.Runtime.PYTHON_3_8, 
                                        code=aws_lambda.Code.from_asset(lamb['folder']),
                                        handler=f'{lamb["file"]}.handler',
                                        role=twitter_lambda_role,
                                        timeout=Duration.seconds(30),
                                        layers=[lambda_layer]
                                        )
            
            for index, expression in enumerate(lamb['cron']):
                rule = aws_events.Rule(self, f'{lamb["name"]}_rule_{index}',
                                        schedule=aws_events.Schedule.expression(f'cron({expression})'))

                rule.add_target(aws_events_targets.LambdaFunction(curr_lambda))