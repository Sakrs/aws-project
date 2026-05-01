import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime', region_name='ap-south-1')
sns = boto3.client('sns')

def lambda_handler(event, context):
    SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:726621696362:Sentry-Alerts"
    
    instance_id = event.get('detail', {}).get('instance-id', 'i-placeholder')
    state = event.get('detail', {}).get('state', 'unknown')
    
    MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0" 
    
    prompt = f"DevOps Alert: EC2 instance {instance_id} has changed to {state} state. Provide a 1-sentence analysis of why this might happen and 1 recommendation for Sakshi."

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    }

    try:
        response = bedrock.invoke_model(modelId=MODEL_ID, body=json.dumps(native_request))
        ai_text = json.loads(response.get('body').read())['content'][0]['text']
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Sentry AI Live Report:\n\nInstance: {instance_id}\nNew State: {state}\n\nAnalysis: {ai_text}",
            Subject=f"Alert: {instance_id} is {state.upper()}"
        )
        
        return {"Status": "Success", "Processed_Instance": instance_id}
        
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}
