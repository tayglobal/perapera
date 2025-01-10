# perapera

Discord Bot for learning a langauge

## Env

To create infra using CloudFormation first create a ``.env``

Add a default region

```
export AWS_DEFAULT_REGION=ap-northeast-1
```


Then source it with

```
source .env
```

## Infra

``cd infra``

1. Install CDK:

```
sudo npm install -g aws-cdk
```

```
pip install --upgrade -r requirements.txt
```

2. Bootstrap (if you haven't already):

```
cdk bootstrap aws://YOUR_ACCOUNT_ID/YOUR_REGION
```

3. Deploy

```
cd cloudformation
cdk deploy \
    --parameters LambdaFunctionMapDev=perapera-dev \
    --parameters LambdaFunctionMapProd=perapera-prod \
    --parameters KmsIdKey=perapera-kms \
    --parameters Stage=dev \
    --parameters BaseTableName=perapera
```
