/** @format */

import {
  Stack,
  StackProps,
  Duration,
  aws_lambda as lambda,
  aws_iam as iam,
  // aws_apigatewayv2,
  // aws_apigatewayv2_integrations,
} from "aws-cdk-lib";
import { Construct } from "constructs";

// CONFIG
const RUNTIME = lambda.Runtime.PYTHON_3_11;
const TIMEOUT = 30;
const APP_DIR_PATH = "../gc_api";
const HANDLER_NAME = "main.handler";
const LAYER_ZIP_PATH = "../dependencies.zip";

export class GoogleCalendarApi extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Lambdaの実行ロールを取得または新規作成
    const role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // Lambda の実行ロールに管理ポリシーを追加
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // 必要に応じて追加の権限をポリシーとしてロールに付与
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["lambda:InvokeFunction", "lambda:InvokeAsync"],
        resources: ["*"],
      })
    );

    // Lambda レイヤーの定義
    const myLayer = new lambda.LayerVersion(this, "Layer", {
      code: lambda.Code.fromAsset(LAYER_ZIP_PATH), // レイヤーの内容を含むディレクトリ
      compatibleRuntimes: [RUNTIME], // このレイヤーが互換性を持つランタイム
    });

    const fn = new lambda.Function(this, "Lambda", {
      runtime: RUNTIME,
      handler: HANDLER_NAME,
      code: lambda.Code.fromAsset(APP_DIR_PATH),
      role: role,
      layers: [myLayer],
      timeout: Duration.seconds(TIMEOUT),
    });

    fn.addEnvironment("GAS_DEPLOY_ID", process.env.GAS_DEPLOY_ID || "");

    fn.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE, // 認証なし
    });

    // // HTTP API の定義
    // const httpApi = new aws_apigatewayv2.HttpApi(this, "ApiGateway");

    // // ルートとインテグレーションの設定
    // httpApi.addRoutes({
    //   path: "/",
    //   methods: [aws_apigatewayv2.HttpMethod.GET],
    //   integration: new aws_apigatewayv2_integrations.HttpLambdaIntegration(
    //     "AppIntegration",
    //     fn
    //   ),
    // });
  }
}
