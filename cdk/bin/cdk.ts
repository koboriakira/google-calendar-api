#!/usr/bin/env node
/** @format */

import "source-map-support/register";
import { App } from "aws-cdk-lib";
import { GoogleCalendarApi } from "../lib/google_calendar_api";
import { Template } from "aws-cdk-lib/assertions";

describe("GoogleCalendarApi Stack", () => {
  const app = new App();
  const stack = new GoogleCalendarApi(app, "TestStack");

  it("creates an IAM role", () => {
    const assert = Template.fromStack(stack);
    assert.resourceCountIs("AWS::IAM::Role", 1);
    assert.hasResourceProperties("AWS::IAM::Role", {
      AssumeRolePolicyDocument: {
        Statement: [
          {
            Action: "sts:AssumeRole",
            Effect: "Allow",
            Principal: {
              Service: "lambda.amazonaws.com",
            },
          },
        ],
        Version: "2012-10-17",
      },
    });
  });

  it("creates a Lambda layer", () => {
    const assert = Template.fromStack(stack);
    assert.resourceCountIs("AWS::Lambda::LayerVersion", 1);
  });

  it("creates a Lambda function", () => {
    const assert = Template.fromStack(stack);
    assert.resourceCountIs("AWS::Lambda::Function", 1);
    assert.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "main.handler",
      Runtime: "python3.11",
    });
  });
});
