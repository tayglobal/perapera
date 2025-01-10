if [[ -v CF_STACK_NAME ]]; then
    echo Creating stack $CF_STACK_NAME
    aws cloudformation create-stack \
    --stack-name $CF_STACK_NAME \
    --template-body file://cf.json \
    --parameters \
        ParameterKey=PolicyName,ParameterValue=PPLambdaPolicy \
        ParameterKey=RoleName,ParameterValue=PPLambdaRole \
        ParameterKey=LambdaFunctionMapDev,ParameterValue=perapera_dev \
        ParameterKey=LambdaFunctionMapProd,ParameterValue=perapera_prod \
        ParameterKey=KmsIdKey,ParameterValue=perapera-kms \
    --capabilities CAPABILITY_NAMED_IAM
else
  echo Must define env var: CF_STACK_NAME
fi