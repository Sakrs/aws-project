Event-Driven Infrastructure Observer

An automated observability pipeline that uses Gen AI to diagnose AWS infrastructure changes in real-time.

# Architecture
This project implements a serverless workflow to monitor the health of instances residing in a highly secure Three-Tier VPC Architecture.

1. Networking Foundation
* VPC Infrastructure: Established a custom VPC with a 10.x.x.x CIDR block, divided into Public and Private Subnets across multiple Availability Zones (AZs) for high availability.
* Secure Access: Configured a Bastion Host in the Public Subnet to act as a secure "jump server" for managing resources in the Private Subnet via SSH.
* Outbound Connectivity: Deployed a NAT Gateway in the Public Subnet, allowing instances in the Private Subnets to securely access the internet (for AI API calls and updates) without exposing them to inbound threats.
* Traffic Management (ELB): Deployed an Application Load Balancer (ALB) in the public subnets to distribute incoming traffic across a fleet of healthy target instances.
* Self-Healing (ASG): Configured an Auto Scaling Group to maintain a desired instance count. The ASG automatically replaces unhealthy instances, ensuring 100% application uptime.


2. Intelligence Pipeline
* Detection: Amazon EventBridge captures EC2 state-change events (Stopped/Terminated) triggered by either manual intervention or Auto Scaling Group (ASG) actions.
* Analysis: An AWS Lambda function (Python/Boto3) is triggered immediately upon event detection.
* Intelligence: The Lambda invokes Amazon Bedrock (Claude 3 Haiku) to perform a real-time diagnostic analysis of the event.
* Notification: The AI-generated report is dispatched via Amazon SNS to a verified email subscriber.

#Tech Stack
- Cloud: AWS (EC2, VPC, EventBridge, Lambda, SNS, IAM)
- Networking: Internet Gateway, NAT Gateway, Bastion Host, Route Tables, Public/Private Subnets.
- AI: Amazon Bedrock (Anthropic Claude 3 Haiku)
- Language: Python 3.x (Boto3)

#Key Concepts Applied
- Secure Networking: Implementing the Bastion Host pattern and NAT Gateway for secure infrastructure management.
- Event-Driven Architecture: Decoupling observation from execution to ensure zero-latency monitoring.
- Principle of Least Privilege: Crafting granular IAM policies for cross-service access between the VPC and AI services.
- AI: Integrating LLMs into standard infrastructure monitoring.
  
Project proof:
  Email received when EC2's state changed:
  <img width="1409" height="381" alt="image" src="https://github.com/user-attachments/assets/75f35a15-ffcb-4390-9c16-6f4e5b45db49" />

  Lambda function:
  <img width="927" height="451" alt="image" src="https://github.com/user-attachments/assets/1d61c934-0dfb-4b1d-b899-acdd079a7331" />

  Triggered rule(Eventbridge):
  <img width="1910" height="685" alt="image" src="https://github.com/user-attachments/assets/64c4d6c0-23c7-45ff-85cc-a6e85c89ed4f" />

  subnet:
  <img width="446" height="503" alt="image" src="https://github.com/user-attachments/assets/bcf02100-cc6d-4989-af42-15108c738dd2" />



