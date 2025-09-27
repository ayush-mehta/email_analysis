# Email Analysis - Daily Summary Lambda

This project provides a serverless AWS Lambda function that runs daily to analyze and summarize emails, sending a summary report via email.

## Architecture

- **AWS Lambda**: Serverless compute for running the daily summary function
- **CloudWatch Events**: Daily cron scheduling (runs at 9:00 AM UTC)
- **AWS SES**: Email sending service
- **Serverless Framework**: Deployment and infrastructure management
- **Poetry**: Python dependency management

## Features

- Daily automated email analysis
- Configurable time ranges for email queries
- Email summary generation and delivery
- CloudWatch logging and monitoring
- Environment-based configuration

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Node.js** (for Serverless Framework)
3. **Python 3.9+**
4. **Poetry** for Python dependency management
5. **AWS CLI** configured with credentials
6. **AWS SES** verified email addresses

## Setup

### 1. Install Dependencies

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install Python dependencies
poetry install

# Install Serverless Framework
npm install -g serverless
npm install serverless-python-requirements
```

### 2. Configure Environment Variables

Copy the example environment file and update with your values:

```bash
cp env.example .env
```

Update the following variables in `.env`:
- `EMAIL_USER`: Your email address for reading emails
- `EMAIL_PASSWORD`: Your email app password
- `SEND_TO_EMAIL`: Recipient email for daily summaries

### 3. AWS SES Setup

1. Verify your sender email address in AWS SES console
2. Verify the recipient email address
3. Request production access if needed (for sending to unverified emails)

### 4. Deploy to AWS

```bash
# Deploy to development environment
serverless deploy

# Deploy to production environment
serverless deploy --stage prod
```

## Configuration

### Cron Schedule

The function runs daily at 9:00 AM UTC. To modify the schedule, update the `rate` in `serverless.yml`:

```yaml
events:
  - schedule:
      rate: cron(0 9 * * ? *)  # 9:00 AM UTC daily
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `EMAIL_USER` | Email address for reading emails | Yes |
| `EMAIL_PASSWORD` | Email app password | Yes |
| `SEND_TO_EMAIL` | Recipient for daily summaries | Yes |

## Usage

### Local Testing

```bash
# Test the function locally
serverless invoke local -f dailySummary
```

### Manual Invocation

```bash
# Invoke the deployed function
serverless invoke -f dailySummary
```

### View Logs

```bash
# View function logs
serverless logs -f dailySummary --tail
```

## Email Provider Integration

The current implementation includes placeholder code for email reading. To integrate with your email provider:

1. **Gmail API**: Use the Gmail API for reading emails
2. **IMAP**: Implement IMAP connection for generic email providers
3. **Exchange**: Use Microsoft Graph API for Office 365

Update the `_read_email` method in `utils/emails.py` with your specific implementation.

## Development

### Project Structure

```
summarise/
├── daily_summary.py          # Main Lambda handler
├── utils/
│   └── emails.py            # Email processing utilities
├── serverless.yml           # Serverless configuration
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Poetry lock file
└── README.md                # This file
```

### Poetry Commands

```bash
# Install dependencies
poetry install

# Add new dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Run in virtual environment
poetry run python daily_summary.py
```

### Adding Features

1. Update the email processing logic in `utils/emails.py`
2. Modify the summary generation in `daily_summary.py`
3. Test locally before deploying
4. Update documentation as needed

## Monitoring

- **CloudWatch Logs**: Function execution logs
- **CloudWatch Metrics**: Invocation count, duration, errors
- **CloudWatch Alarms**: Set up alarms for failures

## Troubleshooting

### Common Issues

1. **SES Sandbox**: Ensure recipient emails are verified in SES
2. **IAM Permissions**: Verify Lambda has SES send permissions
3. **Email Provider**: Check email provider authentication
4. **Cron Schedule**: Verify CloudWatch Events rule is enabled

### Debugging

```bash
# Check function logs
serverless logs -f dailySummary --tail

# Test function locally with debug
serverless invoke local -f dailySummary --log
```

## Security

- Environment variables are encrypted in AWS
- IAM roles follow least privilege principle
- Email credentials should use app passwords, not main passwords
- Consider using AWS Secrets Manager for sensitive data

## Cost Optimization

- Function timeout set to 5 minutes
- Memory allocation optimized for email processing
- CloudWatch log retention can be configured
- Consider using provisioned concurrency for consistent performance

## License

This project is licensed under the MIT License.
