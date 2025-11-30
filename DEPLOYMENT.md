# AWS EC2 Deployment Guide

This guide will help you deploy the Amazon Sentiment Analyzer to AWS EC2.

## Prerequisites

- AWS Account
- Basic knowledge of SSH and command line
- Your project pushed to GitHub

## Step 1: Launch EC2 Instance

1. **Go to AWS EC2 Console**
   - Navigate to https://console.aws.amazon.com/ec2/
   - Click "Launch Instance"

2. **Configure Instance**
   - **Name**: `sentiment-analyzer-app` (or your choice)
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: `t2.small` or `t2.medium` (t2.micro may be too small for model training)
   - **Key Pair**: Create new or select existing SSH key pair (download and save securely!)

3. **Configure Security Group**
   - Click "Edit" next to Network Settings
   - Add the following inbound rules:
     - **SSH**: Port 22, Source: My IP (for security)
     - **Custom TCP**: Port 8501, Source: 0.0.0.0/0 (for Streamlit)
     - **HTTP** (optional): Port 80, Source: 0.0.0.0/0 (if using nginx)

4. **Configure Storage**
   - Set to at least **15-20 GB** (model training needs space)

5. **Launch Instance**
   - Click "Launch Instance"
   - Wait for instance to be in "running" state

## Step 2: Connect to Your Instance

1. **Get Public IP**
   - Go to EC2 Dashboard
   - Select your instance
   - Copy the "Public IPv4 address"

2. **SSH into Instance**
   ```bash
   # Make sure your key has correct permissions
   chmod 400 your-key.pem

   # Connect to instance
   ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
   ```

## Step 3: Automated Setup (Recommended)

Once connected to your EC2 instance:

```bash
# Download the setup script
wget https://raw.githubusercontent.com/YOUR_USERNAME/cs484project/main/setup_ec2.sh

# Make it executable
chmod +x setup_ec2.sh

# Run the setup script
./setup_ec2.sh
```

The script will:
- Install all dependencies
- Clone your repository
- Create a Python virtual environment
- Install Python packages
- Train the model
- Set up the app as a systemd service
- Start the application

**Access your app**: The script will display the URL at the end (e.g., `http://YOUR_IP:8501`)

## Step 4: Manual Setup (Alternative)

If you prefer manual setup:

### 4.1 Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
```

### 4.2 Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/cs484project.git
cd cs484project
```

### 4.3 Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4 Train the Model
```bash
python main.py
```
*This will take several minutes. Wait for completion.*

### 4.5 Test the App
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Visit `http://YOUR_EC2_PUBLIC_IP:8501` to verify it works.

### 4.6 Set Up Systemd Service (for auto-restart)
```bash
# Copy service file
sudo cp streamlit.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

## Step 5: Verify Deployment

1. **Check service status**:
   ```bash
   sudo systemctl status streamlit
   ```

2. **View logs**:
   ```bash
   sudo journalctl -u streamlit -f
   ```

3. **Access the app**:
   - Open browser: `http://YOUR_EC2_PUBLIC_IP:8501`

## Optional: Add Custom Domain with Nginx

### Install Nginx
```bash
sudo apt install -y nginx
```

### Configure Nginx
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/streamlit

# Edit the config to add your domain
sudo nano /etc/nginx/sites-available/streamlit
# Replace 'your-domain.com' with your actual domain

# Enable site
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Update Security Group
- Add inbound rule for HTTP (port 80)

### Point Domain to EC2
- In your domain registrar, create an A record pointing to your EC2 public IP

## Useful Commands

### Service Management
```bash
# Check app status
sudo systemctl status streamlit

# Restart app
sudo systemctl restart streamlit

# Stop app
sudo systemctl stop streamlit

# Start app
sudo systemctl start streamlit

# View logs
sudo journalctl -u streamlit -f
```

### Update App Code
```bash
cd cs484project
git pull
sudo systemctl restart streamlit
```

### Manual Run (for debugging)
```bash
cd cs484project
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## Troubleshooting

### App Not Accessible
- Check security group has port 8501 open
- Verify service is running: `sudo systemctl status streamlit`
- Check logs: `sudo journalctl -u streamlit -f`

### Model Not Found Error
- Ensure model was trained: `ls data/amazon_sentiment_lr_model.joblib`
- If missing, run: `python main.py`

### Out of Memory
- Upgrade to larger instance type (t2.medium or t2.large)
- Or reduce SUBSAMPLE size in main.py before training

### Port 8501 Already in Use
```bash
# Kill existing streamlit processes
pkill -f streamlit
sudo systemctl restart streamlit
```

## Cost Optimization

### Use Elastic IP (Optional)
- Prevents IP change on instance restart
- First Elastic IP is free while instance is running

### Stop Instance When Not in Use
```bash
# From AWS Console or CLI
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

### Use Auto-Scaling (Advanced)
- Set up auto-shutdown during non-business hours
- Use AWS Lambda to start/stop instances on schedule

## Security Best Practices

1. **Restrict SSH Access**
   - Only allow SSH from your IP
   - Use SSH keys, not passwords

2. **Keep System Updated**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Enable HTTPS** (for production)
   - Use Let's Encrypt with Certbot
   - Configure SSL in nginx

4. **Use IAM Roles** (if app needs AWS services)
   - Don't hardcode credentials
   - Attach IAM role to EC2 instance

## Estimated Costs

- **t2.small**: ~$16/month (recommended)
- **t2.medium**: ~$33/month (for heavy usage)
- **Storage (20GB)**: ~$2/month
- **Data Transfer**: Usually free tier covers it

**Total**: ~$18-35/month depending on instance type

## Next Steps

- [ ] Set up automated backups
- [ ] Configure CloudWatch monitoring
- [ ] Add HTTPS with SSL certificate
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling (if needed)
