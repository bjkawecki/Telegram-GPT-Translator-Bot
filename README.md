# Telegram GPT Translator Bot

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/Amazon_Web_Services-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=flat-square&logo=python&logoColor=blue)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat-square&logo=telegram&logoColor=white)
![ChatGPT](https://img.shields.io/badge/OpenApi-74aa9c?style=flat-square&logo=openai&logoColor=white)
![Github-Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

![logo.png](assets/logo.png)

Telegram bot that picks up messages from an input channel, translates them, and forwards them to an output channel.

## Table of Contents

1. **[How it Works](#how-it-works)**
2. **[Requirements](#requirements)**
3. **[Getting Started](#getting-started)**
4. **[Architecture Illustration](#architecture-illustration)**
5. **[Note on the Use of DynamoDB](#note-on-the-use-of-dynamodb)**

## How it Works

- The Telegram bot is subscribed to a source channel. When a new post is published, Telegram sends it via a webhook to an AWS Lambda function.
- The Lambda function extracts the post's text and sends it to the OpenAI API to generate a translated version.
- Once translated, the bot sends the translated post to a designated output channel.

## Requirements

- OpenAI API key
- Telegram Bot Token
- AWS Account

## Getting Started

1. Set up environment variables in `terraform.tfvars`.
2. Deploy infrastructure with Terraform.
3. Push code to trigger deployment.
4. Test locally (optional) with `python main.py` and json test events.

## Architecture Illustration

![architecture-overview.svg](assets/architecture-overview.svg)

## Note on the Use of DynamoDB

The bot differentiates between single-media messages and media groups.
This is because Telegram treats posts with multiple media attachments as media groups, splitting them into multiple events.
To aggregate these related events and reconstruct them into a single message for reposting, DynamoDB is used as temporary storage.
