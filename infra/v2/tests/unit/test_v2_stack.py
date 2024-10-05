import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.v2_stack import V2Stack


# example tests. To run these tests, uncomment this file along with the example
# resource in v2/v2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = V2Stack(app, 'v2')
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
