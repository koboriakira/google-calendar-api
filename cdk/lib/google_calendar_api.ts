/** @format */

import * as cdk from "aws-cdk-lib";
import {
  aws_lambda,
  aws_iam,
  aws_apigatewayv2,
  aws_apigatewayv2_integrations,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import * as fs from "fs";
import * as path from "path";
import * as yaml from "yaml";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class GoogleCalendarApi extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambdaの実行ロールを取得または新規作成
    const role = new aws_iam.Role(this, "LambdaRole", {
      assumedBy: new aws_iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // Lambda の実行ロールに管理ポリシーを追加
    role.addManagedPolicy(
      aws_iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // 必要に応じて追加の権限をポリシーとしてロールに付与
    role.addToPrincipalPolicy(
      new aws_iam.PolicyStatement({
        actions: ["lambda:InvokeFunction", "lambda:InvokeAsync"],
        resources: ["*"],
      })
    );

    // Lambda レイヤーの定義
    const myLayer = new aws_lambda.LayerVersion(this, "Layer", {
      code: aws_lambda.Code.fromAsset("../dependencies.zip"), // レイヤーの内容を含むディレクトリ
      compatibleRuntimes: [aws_lambda.Runtime.PYTHON_3_11], // このレイヤーが互換性を持つランタイム
    });

    const fn = new aws_lambda.Function(this, "Lambda", {
      runtime: aws_lambda.Runtime.PYTHON_3_11,
      handler: "main.handler",
      code: aws_lambda.Code.fromAsset("../gc_api"),
      role: role,
      layers: [myLayer],
      timeout: cdk.Duration.seconds(30),
    });

    fn.addEnvironment("GAS_DEPLOY_ID", process.env.GAS_DEPLOY_ID || "");

    fn.addFunctionUrl({
      authType: aws_lambda.FunctionUrlAuthType.NONE, // 認証なし
    });

    // // HTTP API の定義
    // const httpApi = new aws_apigatewayv2.HttpApi(this, "ApiGateway");

    // // ルートとインテグレーションの設定
    // httpApi.addRoutes({
    //   path: "/hello",
    //   methods: [aws_apigatewayv2.HttpMethod.GET],
    //   integration: new aws_apigatewayv2_integrations.HttpLambdaIntegration(
    //     "HelloIntegration",
    //     fn
    //   ),
    // });

    // httpApi.addRoutes({
    //   path: "/list",
    //   methods: [aws_apigatewayv2.HttpMethod.GET],
    //   integration: new aws_apigatewayv2_integrations.HttpLambdaIntegration(
    //     "ListIntegration",
    //     fn
    //   ),
    // });
  }
}
