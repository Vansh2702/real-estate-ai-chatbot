import boto3
import json

runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

prompt = {
  "messages": [
    {"role": "user", "content": "Give me 5 real estate investment tips"}
  ],
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 1000
}

response = runtime.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",  # or any from your list
    contentType="application/json",
    accept="application/json",
    body=json.dumps(prompt)
)

output = json.loads(response['body'].read())
print(output['content'][0]['text'])
