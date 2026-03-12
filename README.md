# DevOps Log Cleanup Automation

## Overview

This project automates log management for Linux application servers. Over time, log files in `/var/log` can accumulate and consume disk space. This script automatically detects old log files, backs them up to AWS S3 for compliance, deletes them locally, and sends an execution report via AWS SES email notification.

The automation ensures that servers remain storage-efficient while preserving logs for auditing and monitoring purposes.

---

# Architecture

EC2 Instance
↓
Python Script (`log_cleanup.py`)
↓
Scan `/var/log` for `.log` files older than 30 days
↓
Upload logs to AWS S3
↓
Delete logs locally after successful upload
↓
Send execution report via AWS SES

---

# Features

* Detect `.log` files older than **30 days**
* Upload logs to **AWS S3**
* Delete local files **only after successful upload**
* Error handling for S3 failures or file permissions
* Email notification using **AWS SES**
* Secure authentication using **IAM roles**
* Can be scheduled automatically using **cron**

---

# Technologies Used

* Python 3
* AWS S3
* AWS SES
* IAM Roles
* EC2
* Cron (Linux scheduler)
* boto3 (AWS SDK for Python)

---

# Prerequisites

Before running the script, ensure the following:

### 1. AWS Services

Create the following AWS resources:

* **S3 Bucket**
  Example:

```
logs-backup
```

* **IAM Role** attached to EC2 instance with permissions:

```
s3:PutObject
ses:SendEmail
```

* **AWS SES**
  Verify the sender email address.

Example sender:

```
your-email@gmail.com
```

---

### 2. Install Python Dependencies

Install boto3:

```
pip3 install boto3
```

---

# Step-by-Step Execution

## Step 1 — Launch EC2 Instance

Create an EC2 instance running Linux (Ubuntu).

Example configuration:

* Ubuntu 22.04
* t2.micro

---

## Step 2 — Create S3 Bucket

Go to:

AWS Console → S3 → Create Bucket

Example bucket name:

```
logs-backup
```

---

## Step 3 — Configure IAM Role

Create an IAM Role for EC2 with permissions:

```
S3
    s3:PutObject

SES
    ses:SendEmail
```

Attach the role to the EC2 instance.

---

## Step 4 — Upload the Script

SSH into the EC2 instance:

```
ssh ubuntu@<EC2_PUBLIC_IP>
```

Create the script:

```
nano log_cleanup.py
```

Paste the Python script and save.

---

## Step 5 — Test Script

Run the script manually:

```
sudo python3 log_cleanup.py
```

Expected behavior:

1. Script scans `/var/log`
2. Detects `.log` files older than 30 days
3. Uploads them to S3
4. Deletes them locally
5. Sends email notification

Example email report:

```
Log Cleanup Report

Uploaded & deleted: /var/log/demo.log
```

---

# Automating the Script

To run the script automatically every day at midnight:

Open crontab:

```
crontab -e
```

Add the following line:

```
0 0 * * * sudo python3 /home/ubuntu/log_cleanup.py
```

This schedules the script to run **daily at midnight**.

---

# Deployment Across Multiple EC2 Instances

For a fleet of 50+ EC2 servers, the script can be deployed using:

### AWS Systems Manager (Recommended)

Use **SSM State Manager** to distribute and schedule the script across instances.

Advantages:

* No SSH required
* Centralized management
* Tag-based instance targeting

---

### Alternative Methods

**AMI Based Deployment**

* Bake script and cron job into AMI.

**Configuration Management**

* Use Ansible or Terraform.

---

# Error Handling

The script handles common failure cases:

| Scenario              | Behavior                |
| --------------------- | ----------------------- |
| S3 upload failure     | File is not deleted     |
| File permission error | Logged in execution log |
| SES email failure     | Error logged            |
| No old logs found     | Email still sent        |

Example message:

```
No log files older than 30 days found.
```

---

# Security Best Practices

The solution follows DevOps security best practices:

* No hardcoded AWS access keys
* Uses **IAM roles**
* Principle of least privilege
* Logs execution results

---

# Future Improvements

Possible enhancements:

* Compress logs before uploading
* Add log rotation
* Upload logs to date-based S3 folders
* Add CloudWatch monitoring
* Use Lambda instead of cron

---

# Author

Srivenkatesh
DevOps Intern Assessment Project
