#!/bin/sh

#set -x

cd /usr/tsunami

if [ $# -eq 0 ] ; then
    echo 'No argument passed to script'
    exit 1
fi

IP_V4_TARGET=$1
TARGET_ARGS="--ip-v4-target=${IP_V4_TARGET}"
IP_CHANGE=$(echo "$IP_V4_TARGET" | sed 's/\./\_/g')
OUTPUT_FNAME="$IP_CHANGE-`date "+%Y_%m_%d_%H%M"`.json"
echo -e "output filename: $OUTPUT_FNAME"

java -cp tsunami.jar:plugins/* -Dtsunami-config.location=tsunami.yaml \
  com.google.tsunami.main.cli.TsunamiCli \
  ${TARGET_ARGS} \
  --scan-results-local-output-format=JSON --scan-results-local-output-filename=${OUTPUT_FNAME}

cat ${OUTPUT_FNAME}
echo -e "upload $OUTPUT_FNAME to S3"
if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q 'NoSuchBucket'
then
    aws s3api create-bucket --bucket "$S3_BUCKET" --region "$AWS_REGION"
    sleep 2
fi
aws s3 cp "$OUTPUT_FNAME" s3://"$S3_BUCKET"/"$OUTPUT_FNAME"
