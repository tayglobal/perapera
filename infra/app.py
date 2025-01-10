import aws_cdk as cdk
from aws_cdk import (
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    Stack,
    CfnOutput
)
from constructs import Construct

class PeraPeraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameters
        # app_name = cdk.CfnParameter(self, "AppName", type="String",
        #                               description="The name of the App", default="PeraPera")

        # app_name_str = app_name.value_as_string

        app_name_str = 'PeraPera'
        lower_app_name = app_name_str.lower()

        role_name = app_name_str + "Role"
        kms_id_key = app_name_str + "KMS"
        policy_name = app_name_str + "Policy"

        base_table_name = lower_app_name

        # Construct Lambda function names
        lambda_function_map_dev = f"{lower_app_name}-dev"
        lambda_function_map_prod = f"{lower_app_name}-prod"

        # IAM Role
        my_iam_role = iam.Role(
            self, role_name,
            role_name=role_name,
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
                iam.ServicePrincipal("apigateway.amazonaws.com")
            )
        )
        
        # Managed Policy
        my_iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute"))
        
        # IAM Policy
        iam.Policy(
            self, "IAMPolicy",
            policy_name=policy_name,
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "dynamodb:BatchGet*",
                        "dynamodb:DescribeStream",
                        "dynamodb:DescribeTable",
                        "dynamodb:Get*",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:BatchWrite*",
                        "dynamodb:CreateTable",
                        "dynamodb:Delete*",
                        "dynamodb:Update*",
                        "dynamodb:PutItem"
                    ],
                    resources=[f"arn:aws:dynamodb:{self.region}:{self.account}:table/{base_table_name}-*"]
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    resources=["arn:aws:logs:*:*:*"]
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["lambda:InvokeFunction"],
                    resources=[
                        f"arn:aws:lambda:{self.region}:{self.account}:function:{lambda_function_map_dev}",
                        f"arn:aws:lambda:{self.region}:{self.account}:function:{lambda_function_map_prod}"
                    ]
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "kms:Encrypt",
                        "kms:Decrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*",
                        "kms:DescribeKey"
                    ],
                    resources=[f"arn:aws:kms:{self.region}:{self.account}:key/{kms_id_key}"]
                )
            ],
            roles=[my_iam_role]
        )

        # DynamoDB Tables
        dynamodb_table_dev = dynamodb.Table(
            self, "DynamoDBTableDev",
            table_name=f"{base_table_name}-dev",
            partition_key=dynamodb.Attribute(name="path", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY # Be careful with this in production
        )

        dynamodb_table_prod = dynamodb.Table(
            self, "DynamoDBTableProd",
            table_name=f"{base_table_name}-prod",
            partition_key=dynamodb.Attribute(name="path", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY # Be careful with this in production
        )

        dynamodb_table_dev.add_global_secondary_index(
            index_name="folder-index",
            partition_key=dynamodb.Attribute(name="folder", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL
        )

        dynamodb_table_prod.add_global_secondary_index(
            index_name="folder-index",
            partition_key=dynamodb.Attribute(name="folder", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL
        )

        # Outputs to easily retrieve the table names
        CfnOutput(self, "DynamoDBTableNameOutputDev", 
                  value=dynamodb_table_dev.table_name,
                  description="DynamoDB Table Name for Dev")

        CfnOutput(self, "DynamoDBTableNameOutputProd", 
                  value=dynamodb_table_prod.table_name,
                  description="DynamoDB Table Name for Prod")


if __name__ == '__main__':
    app = cdk.App()
    PeraPeraStack(app, 'PeraPera' + "Stack")
    app.synth()