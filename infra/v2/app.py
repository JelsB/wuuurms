#!/usr/bin/env python
import aws_cdk as cdk
from stacks.api_stack import ApiStack


app = cdk.App()
ApiStack(app, 'Api', env={'account': '016957204234', 'region': 'eu-central-1'})

app.synth()
