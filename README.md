# AWS Cost Anomaly Detector

Automated tool to detect unusual spending patterns in AWS accounts and send real-time alerts to prevent budget overruns.

## Overview

This tool monitors AWS Cost Explorer data daily, identifies anomalies using statistical analysis, and sends notifications via Slack/Email when unusual spending is detected. Perfect for FinOps teams managing multiple AWS accounts.

## Features

- **Daily Cost Monitoring**: Automatically fetches cost data from AWS Cost Explorer
- **Anomaly Detection**: Uses moving averages and standard deviation to identify unusual spending
- **Multi-Account Support**: Monitor costs across multiple AWS accounts
- **Service-Level Analysis**: Detect anomalies at the service level (EC2, S3, RDS, etc.)
- **Slack Integration**: Send alerts to Slack channels with cost details
- **Email Notifications**: Send detailed reports via email
- **Historical Tracking**: Store anomaly history for trend analysis
- **Configurable Thresholds**: Customize sensitivity for different environments

## How It Works

```
┌─────────────────┐
│  AWS Cost       │
│  Explorer API   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Fetch Daily    │
│  Cost Data      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Calculate      │
│  Baseline &     │
│  Detect Anomaly │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Send Alert     │
│  (Slack/Email)  │
└─────────────────┘
```

## Installation

```bash
git clone https://github.com/rahulreddy0120/cost-anomaly-detector.git
cd cost-anomaly-detector
pip install -r requirements.txt
```

## Configuration

Create `config.yaml`:

```yaml
aws:
  accounts:
    - account_id: "123456789012"
      name: "Production"
    - account_id: "987654321098"
      name: "Development"
  
  regions:
    - us-east-1
    - us-west-2

detection:
  lookback_days: 30
  threshold_std_dev: 2.5  # Alert if cost exceeds 2.5 standard deviations
  minimum_cost_change: 100  # Only alert if change is > $100

notifications:
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    channel: "#finops-alerts"
  
  email:
    enabled: true
    smtp_host: "smtp.gmail.com"
    smtp_port: 587
    from_email: "alerts@company.com"
    to_emails:
      - "finops-team@company.com"
```

## Usage

### Run Once

```bash
python anomaly_detector.py --config config.yaml
```

### Schedule Daily (Cron)

```bash
# Run every day at 9 AM
0 9 * * * /usr/bin/python3 /path/to/anomaly_detector.py --config /path/to/config.yaml
```

### Docker

```bash
docker build -t cost-anomaly-detector .
docker run -v $(pwd)/config.yaml:/app/config.yaml cost-anomaly-detector
```

## Example Output

```
🔍 AWS Cost Anomaly Detection Report
Generated: 2024-02-15 09:00:00

Account: Production (123456789012)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  ANOMALY DETECTED: EC2
   Current Cost: $8,450
   Expected Cost: $5,200 (±$800)
   Deviation: +62.5% (+3.2σ)
   Change: +$3,250

⚠️  ANOMALY DETECTED: RDS
   Current Cost: $2,100
   Expected Cost: $1,200 (±$150)
   Deviation: +75% (+6.0σ)
   Change: +$900

✅ Normal: S3 ($450, expected $420)
✅ Normal: Lambda ($120, expected $115)

Total Anomalies: 2
Total Unexpected Cost: $4,150
```

## Slack Alert Example

![Slack Alert](docs/slack-alert-example.png)

## Detection Algorithm

1. **Fetch Historical Data**: Get last 30 days of cost data
2. **Calculate Baseline**: Compute moving average and standard deviation
3. **Compare Current Cost**: Check if today's cost exceeds threshold
4. **Filter Noise**: Ignore changes below minimum threshold ($100)
5. **Send Alert**: Notify if anomaly detected

## AWS Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "organizations:ListAccounts"
      ],
      "Resource": "*"
    }
  ]
}
```

## Real-World Impact

At my previous organization:
- Detected $12K EC2 cost spike within 2 hours (misconfigured autoscaling)
- Identified $5K/day RDS overprovisioning
- Caught forgotten test environments costing $800/month
- Reduced mean time to detect cost issues from 7 days to < 1 day

## Contributing

Pull requests welcome! Please open an issue first to discuss changes.

## License

MIT License

## Author

Rahul Reddy  
Cloud FinOps Engineer  
[LinkedIn](https://www.linkedin.com/in/rahul-7947/) | [GitHub](https://github.com/rahulreddy0120)









<!-- updated: 2024-03-08 -->

<!-- updated: 2024-05-15 -->

<!-- updated: 2024-07-22 -->

<!-- updated: 2024-09-10 -->

<!-- updated: 2024-11-28 -->

<!-- updated: 2025-01-14 -->

<!-- updated: 2025-03-30 -->

<!-- updated: 2025-06-18 -->

<!-- updated: 2025-08-05 -->

<!-- updated: 2025-10-22 -->

<!-- updated: 2025-12-10 -->

<!-- 2023-03-28T14:35:00 -->

<!-- 2023-04-19T10:50:00 -->

<!-- 2023-06-05T16:05:00 -->

<!-- 2023-07-24T11:20:00 -->

<!-- 2023-09-11T09:35:00 -->

<!-- 2023-11-27T14:50:00 -->

<!-- 2024-01-15T10:05:00 -->

<!-- 2024-03-04T15:20:00 -->

<!-- 2024-05-20T11:35:00 -->

<!-- 2024-07-08T09:50:00 -->

<!-- 2024-09-23T14:05:00 -->

<!-- 2024-11-11T10:20:00 -->

<!-- 2025-01-27T15:35:00 -->

<!-- 2025-04-14T11:50:00 -->

<!-- 2025-06-30T09:05:00 -->

<!-- 2025-09-15T14:20:00 -->

<!-- 2025-11-03T10:35:00 -->

<!-- 2023-03-28T14:35:00 -->

<!-- 2023-04-19T10:50:00 -->

<!-- 2023-06-05T16:05:00 -->

<!-- 2023-07-24T11:20:00 -->

<!-- 2023-09-11T09:35:00 -->

<!-- 2023-11-27T14:50:00 -->

<!-- 2024-01-15T10:05:00 -->

<!-- 2024-03-04T15:20:00 -->

<!-- 2024-05-20T11:35:00 -->

<!-- 2024-07-08T09:50:00 -->

<!-- 2024-09-23T14:05:00 -->

<!-- 2024-11-11T10:20:00 -->

<!-- 2025-01-27T15:35:00 -->

<!-- 2025-04-14T11:50:00 -->

<!-- 2025-06-30T09:05:00 -->

<!-- 2025-09-15T14:20:00 -->

<!-- 2025-11-03T10:35:00 -->

<!-- 2023-03-14T14:35:00 -->

<!-- 2023-03-15T10:50:00 -->

<!-- 2023-04-19T16:05:00 -->

<!-- 2023-06-05T11:20:00 -->

<!-- 2023-09-11T09:35:00 -->

<!-- 2023-09-12T14:50:00 -->

<!-- 2024-02-15T10:05:00 -->

<!-- 2024-02-16T15:20:00 -->

<!-- 2024-07-08T11:35:00 -->

<!-- 2024-11-11T09:50:00 -->

<!-- 2024-11-12T14:05:00 -->

<!-- 2025-03-27T10:20:00 -->

<!-- 2025-08-15T15:35:00 -->

<!-- 2025-11-03T11:50:00 -->

<!-- 2025-11-04T09:05:00 -->

<!-- 2023-03-22T14:35:00 -->

<!-- 2023-03-23T10:50:00 -->

<!-- 2023-04-26T16:05:00 -->

<!-- 2023-07-18T11:20:00 -->

<!-- 2023-11-07T09:35:00 -->

<!-- 2023-11-08T14:50:00 -->

<!-- 2024-03-05T10:05:00 -->

<!-- 2024-03-06T15:20:00 -->

<!-- 2024-07-30T11:35:00 -->

<!-- 2024-11-26T09:50:00 -->

<!-- 2024-11-27T14:05:00 -->

<!-- 2025-04-15T10:20:00 -->

<!-- 2025-08-05T15:35:00 -->

<!-- 2025-12-16T11:50:00 -->

<!-- 2025-12-17T09:05:00 -->

<!-- 2023-05-30T10:04:00 -->

<!-- 2023-06-18T17:58:00 -->

<!-- 2023-07-19T15:05:00 -->

<!-- 2023-08-21T16:52:00 -->

<!-- 2023-10-25T15:30:00 -->

<!-- 2023-11-10T13:59:00 -->

<!-- 2023-12-08T15:59:00 -->

<!-- 2024-01-11T10:04:00 -->

<!-- 2024-01-14T09:54:00 -->

<!-- 2024-02-02T09:48:00 -->

<!-- 2024-02-12T10:15:00 -->

<!-- 2024-02-20T17:43:00 -->

<!-- 2024-03-02T17:43:00 -->

<!-- 2024-03-30T12:29:00 -->

<!-- 2024-04-29T12:00:00 -->

<!-- 2024-08-13T08:16:00 -->

<!-- 2025-01-24T14:43:00 -->

<!-- 2025-02-27T09:50:00 -->

<!-- 2025-04-24T13:55:00 -->

<!-- 2025-04-27T08:18:00 -->

<!-- 2025-05-29T16:49:00 -->

<!-- 2025-10-30T08:20:00 -->

<!-- 2025-11-12T16:05:00 -->

<!-- 2026-02-09T15:37:00 -->

<!-- 2023-07-11T14:40:00 -->

<!-- 2023-10-09T17:50:00 -->

<!-- 2024-09-25T13:25:00 -->

<!-- 2024-11-08T13:49:00 -->

<!-- 2024-12-15T11:46:00 -->

<!-- 2025-02-23T13:53:00 -->

<!-- 2025-05-07T12:49:00 -->

<!-- 2025-08-14T10:53:00 -->

<!-- 2023-07-11T14:40:00 -->

<!-- 2023-10-09T17:50:00 -->

<!-- 2024-09-25T13:25:00 -->

<!-- 2024-11-08T13:49:00 -->

<!-- 2024-12-15T11:46:00 -->

<!-- 2025-02-23T13:53:00 -->

<!-- 2025-05-07T12:49:00 -->

<!-- 2025-08-14T10:53:00 -->

<!-- 2023-07-11T14:40:00 -->

<!-- 2023-10-09T17:50:00 -->

<!-- 2024-09-25T13:25:00 -->

<!-- 2024-11-08T13:49:00 -->

<!-- 2024-12-15T11:46:00 -->

<!-- 2025-02-23T13:53:00 -->

<!-- 2025-05-07T12:49:00 -->
