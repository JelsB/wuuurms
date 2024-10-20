#!/usr/bin/env python
import aws_cdk as cdk
from stacks.api_stack import ApiStack
from stacks.databases_stack import DatabasesStack


app = cdk.App()
env = {'account': '016957204234', 'region': 'eu-central-1'}
databases = DatabasesStack(app, 'Databases', env=env)
api = ApiStack(app, 'Api', tables=databases.tables, env=env)
app.synth()
