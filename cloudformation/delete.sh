if [[ -v CF_STACK_NAME ]]; then
    echo Deleting stack $CF_STACK_NAME
    aws cloudformation delete-stack --stack-name $CF_STACK_NAME
else
  echo Must define env var: CF_STACK_NAME
fi
