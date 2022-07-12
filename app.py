#!/usr/bin/env python3

import aws_cdk as cdk

from procyon.procyon_stack import ProcyonStack


app = cdk.App()
ProcyonStack(app, "procyon")

app.synth()
