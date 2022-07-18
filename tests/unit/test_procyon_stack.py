import aws_cdk as core
import aws_cdk.assertions as assertions
from procyon.procyon_stack import ProcyonStack


def test_lambda_created():
    app = core.App()
    stack = ProcyonStack(app, 'procyon')
    template = assertions.Template.from_stack(stack)

    template.resource_count_is('AWS::IAM::Role', 1)
    template.resource_count_is('AWS::Lambda::Function', 1)
    template.resource_count_is('AWS::Lambda::LayerVersion', 1)