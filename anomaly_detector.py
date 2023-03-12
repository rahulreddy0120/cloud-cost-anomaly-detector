#!/usr/bin/env python3
"""
AWS Cost Anomaly Detector
Monitors AWS spending and alerts on unusual patterns
"""

import boto3
import yaml
import json
import requests
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from statistics import mean, stdev
import argparse

class CostAnomalyDetector:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.ce_client = boto3.client('ce')
        
    def get_cost_data(self, account_id, days=30):
        """Fetch cost data for the last N days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ],
            Filter={
                'Dimensions': {
                    'Key': 'LINKED_ACCOUNT',
                    'Values': [account_id]
                }
            }
        )
        
        # Parse response into structured data
        cost_by_service = {}
        
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            
            for group in result.get('Groups', []):
                service = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                
                if service not in cost_by_service:
                    cost_by_service[service] = []
                
                cost_by_service[service].append({
                    'date': date,
                    'cost': cost
                })
        
        return cost_by_service
    
    def detect_anomalies(self, cost_data):
        """Detect anomalies using statistical analysis"""
        anomalies = []
        threshold = self.config['detection']['threshold_std_dev']
        min_change = self.config['detection']['minimum_cost_change']
        
        for service, data in cost_data.items():
            if len(data) < 7:  # Need at least a week of data
                continue
            
            # Get historical costs (exclude today)
            historical_costs = [d['cost'] for d in data[:-1]]
            current_cost = data[-1]['cost']
            
            if len(historical_costs) < 2:
                continue
            
            # Calculate baseline
            avg_cost = mean(historical_costs)
            std_cost = stdev(historical_costs) if len(historical_costs) > 1 else 0
            
            # Detect anomaly
            if std_cost > 0:
                deviation = (current_cost - avg_cost) / std_cost
                cost_change = current_cost - avg_cost
                
                if abs(deviation) > threshold and abs(cost_change) > min_change:
                    anomalies.append({
                        'service': service,
                        'current_cost': current_cost,
                        'expected_cost': avg_cost,
                        'std_dev': std_cost,
                        'deviation': deviation,
                        'cost_change': cost_change,
                        'percentage_change': (cost_change / avg_cost * 100) if avg_cost > 0 else 0
                    })
        
        return anomalies
    
    def send_slack_alert(self, account_name, anomalies):
        """Send alert to Slack"""
        if not self.config['notifications']['slack']['enabled']:
            return
        
        webhook_url = self.config['notifications']['slack']['webhook_url']
        
        # Build message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"⚠️ Cost Anomaly Detected: {account_name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{len(anomalies)} anomalies* detected on {datetime.now().strftime('%Y-%m-%d')}"
                }
            }
        ]
        
        for anomaly in anomalies[:5]:  # Limit to 5 for readability
            direction = "📈" if anomaly['cost_change'] > 0 else "📉"
            blocks.append({
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Service:*\n{anomaly['service']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Current Cost:*\n${anomaly['current_cost']:.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Expected:*\n${anomaly['expected_cost']:.2f} (±${anomaly['std_dev']:.2f})"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Change:*\n{direction} ${abs(anomaly['cost_change']):.2f} ({anomaly['percentage_change']:+.1f}%)"
                    }
                ]
            })
            blocks.append({"type": "divider"})
        
        payload = {
            "channel": self.config['notifications']['slack']['channel'],
            "blocks": blocks
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print(f"✅ Slack alert sent for {account_name}")
            else:
                print(f"❌ Failed to send Slack alert: {response.status_code}")
        except Exception as e:
            print(f"❌ Error sending Slack alert: {e}")
    
    def send_email_alert(self, account_name, anomalies):
        """Send alert via email"""
        if not self.config['notifications']['email']['enabled']:
            return
        
        smtp_config = self.config['notifications']['email']
        
        # Build email body
        body = f"""
        <html>
        <body>
        <h2>AWS Cost Anomaly Alert: {account_name}</h2>
        <p>Detected {len(anomalies)} cost anomalies on {datetime.now().strftime('%Y-%m-%d')}</p>
        
        <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Service</th>
            <th>Current Cost</th>
            <th>Expected Cost</th>
            <th>Change</th>
            <th>Deviation</th>
        </tr>
        """
        
        for anomaly in anomalies:
            body += f"""
            <tr>
                <td>{anomaly['service']}</td>
                <td>${anomaly['current_cost']:.2f}</td>
                <td>${anomaly['expected_cost']:.2f} (±${anomaly['std_dev']:.2f})</td>
                <td>${anomaly['cost_change']:+.2f} ({anomaly['percentage_change']:+.1f}%)</td>
                <td>{anomaly['deviation']:+.2f}σ</td>
            </tr>
            """
        
        body += """
        </table>
        </body>
        </html>
        """
        
        # Send email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"⚠️ Cost Anomaly Alert: {account_name}"
        msg['From'] = smtp_config['from_email']
        msg['To'] = ', '.join(smtp_config['to_emails'])
        
        msg.attach(MIMEText(body, 'html'))
        
        try:
            with smtplib.SMTP(smtp_config['smtp_host'], smtp_config['smtp_port']) as server:
                server.starttls()
                # In production, use proper authentication
                server.send_message(msg)
            print(f"✅ Email alert sent for {account_name}")
        except Exception as e:
            print(f"❌ Error sending email: {e}")
    
    def run(self):
        """Main execution"""
        print(f"🔍 AWS Cost Anomaly Detection")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        total_anomalies = 0
        
        for account in self.config['aws']['accounts']:
            account_id = account['account_id']
            account_name = account['name']
            
            print(f"\n📊 Analyzing: {account_name} ({account_id})")
            
            # Fetch cost data
            cost_data = self.get_cost_data(
                account_id, 
                days=self.config['detection']['lookback_days']
            )
            
            # Detect anomalies
            anomalies = self.detect_anomalies(cost_data)
            
            if anomalies:
                print(f"⚠️  Found {len(anomalies)} anomalies:")
                for anomaly in anomalies:
                    print(f"   - {anomaly['service']}: "
                          f"${anomaly['current_cost']:.2f} "
                          f"(expected ${anomaly['expected_cost']:.2f}, "
                          f"{anomaly['deviation']:+.1f}σ)")
                
                # Send notifications
                self.send_slack_alert(account_name, anomalies)
                self.send_email_alert(account_name, anomalies)
                
                total_anomalies += len(anomalies)
            else:
                print("✅ No anomalies detected")
        
        print("\n" + "=" * 60)
        print(f"Total anomalies detected: {total_anomalies}")
        
        return total_anomalies

def main():
    parser = argparse.ArgumentParser(description='AWS Cost Anomaly Detector')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    detector = CostAnomalyDetector(config_file=args.config)
    detector.run()

if __name__ == '__main__':
    main()
