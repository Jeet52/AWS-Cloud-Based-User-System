
# 🚀 E2E User Management System - Deployment Walkthrough

**Location:** IT Expert Schaumburg  
**Date:** July 15, 2025  
**Time:** 2:15 PM  

---

## 1) AWS ACCOUNT & TOOLS

- Website: [aws.amazon.com](https://aws.amazon.com)
- Services used: EC2 Instance and RDS (MySQL) Database
- Other Tools: MySQL Workbench, Python3, Postman

---

## 2) LAUNCH EC2 INSTANCE

1. Login to AWS Console → Search **EC2** → Click **EC2**
2. Click **Launch Instance**
3. Configure:
   - **Name**: FlaskServer
   - **AMI**: Ubuntu 20.04
   - **Instance Type**: t3.micro (Free Tier)
   - **Key Pair**: Create new → download `.pem` file
   - **Security Group**: Allow inbound ports 22 (SSH), 80 (HTTP)
4. Click **Launch Instance**
5. Copy Public IPv4 address of the instance

---

## 3) SET UP SERVER (SSH & INSTALL PACKAGES)

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<your-ec2-ip>

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
pip3 install flask mysql-connector-python
```

---

## 4) CREATE RDS MYSQL DATABASE

1. Go to **RDS Dashboard** → Click **Create Database**
2. Select:
   - **Engine**: MySQL (latest version)
   - **Templates**: Free tier
   - **DB Instance Identifier**: userdb
   - **Username**: admin
   - **Password**: (strong password)
3. Connectivity Settings:
   - **Public access**: Enabled
   - **VPC security group**: Create new → Name: `rds-mysql-open`
4. After DB is created:
   - Modify Inbound Rules of its Security Group
   - Add rule: MySQL/Aurora | TCP | Port 3306 | Source: your EC2's IP (e.g. `X.X.X.X/32`)

---

## 5) BUILD FLASK PROJECT & MYSQL TABLE

```bash
mkdir user-management
cd user-management
nano app.py

mkdir templates
nano templates/register.html

mysql -h <rds-endpoint> -u admin -p

# Inside MySQL
CREATE DATABASE userdb;
USE userdb;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Run Flask app:
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```
Visit in browser: `http://<ec2-public-ip>:5000/register`

---

## 6) TESTING WITH POSTMAN

- **POST** to `/register`:
```json
{
  "username": "postman_user",
  "password": "12345",
  "first_name": "Postman",
  "last_name": "Test",
  "email": "postman@example.com"
}
```

- **GET** `/api/users` to view all users

---

## 7) SAVE CODE TO GITHUB

```bash
git init
git remote add origin https://github.com/<your-username>/flask-user-management.git

# Add your project files
touch requirements.txt .gitignore README.md
git add .
git commit -m "Initial commit: Flask user management system"
git push -u origin main
```

Recommended files:
- `README.md`
- `WALKTHROUGH.md` (this file)
- `requirements.txt`
- `.gitignore`

---

## 8) AVOID AWS COSTS

| Resource         | Possible Charges                  | Where to Check                   |
|------------------|----------------------------------|----------------------------------|
| EBS Volumes      | If not deleted after EC2 stop    | EC2 Dashboard → Volumes          |
| Snapshots        | If created manually               | EC2 & RDS Dashboards             |
| Elastic IPs      | If not attached to a running EC2 | EC2 Dashboard → Elastic IPs      |
| S3 Buckets       | If you uploaded files             | S3 Dashboard → Buckets           |
| CloudWatch Logs  | EC2 or RDS logs                   | CloudWatch → Log groups          |
| Load Balancers   | Charged hourly                    | EC2 Dashboard → Load Balancers   |
| VPC Endpoints    | Often forgotten, costly           | VPC Dashboard                    |
| Data Transfer    | Large outbound transfers          | Billing → Cost Explorer          |

---

**✅ End of Walkthrough**  
For questions or issues, open an issue on the GitHub repo.
