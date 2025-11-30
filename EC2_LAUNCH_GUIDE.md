# Step-by-Step Guide: Launching an EC2 Instance

## Step 1: Access AWS Console

1. Go to [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
2. Sign in to your AWS account
3. Make sure you're in your preferred region (top-right corner, e.g., "US East (N. Virginia)")

## Step 2: Navigate to EC2

1. In the AWS Console search bar at the top, type "EC2"
2. Click on "EC2" (Virtual Servers in the Cloud)
3. Click the orange "Launch instance" button

## Step 3: Name Your Instance

In the "Name and tags" section:
- **Name**: Enter something like `sentiment-analyzer-app` or `my-streamlit-app`

## Step 4: Choose Operating System (AMI)

In the "Application and OS Images (Amazon Machine Image)" section:

1. Click on "Quick Start" (should be selected by default)
2. Select **"Ubuntu"**
3. From the dropdown, choose **"Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"**
4. Architecture: **64-bit (x86)**
5. Make sure it says "Free tier eligible" if you want to stay in free tier

## Step 5: Choose Instance Type

In the "Instance type" section:

**For this project, choose one of:**
- **t2.small** (1 vCPU, 2 GB RAM) - **RECOMMENDED** (~$16/month)
  - Good for training the model and running the app
- **t2.medium** (2 vCPU, 4 GB RAM) - If you want faster performance (~$33/month)

**Note**: t2.micro (free tier) has only 1GB RAM and may crash during model training

Click the dropdown and search/select your preferred type.

## Step 6: Create/Select Key Pair (IMPORTANT!)

In the "Key pair (login)" section:

### If you don't have a key pair yet:

1. Click "Create new key pair"
2. **Key pair name**: Enter something like `my-ec2-key` or `sentiment-app-key`
3. **Key pair type**: RSA
4. **Private key file format**:
   - Select **.pem** if you're on Mac/Linux
   - Select **.ppk** if you're on Windows using PuTTY
5. Click "Create key pair"
6. **IMPORTANT**: The .pem file will download automatically - SAVE IT SAFELY!
   - Move it to a secure location like `~/.ssh/` on Mac/Linux
   - You'll need this file to SSH into your instance
   - You cannot download it again!

### If you already have a key pair:
- Select it from the dropdown

## Step 7: Configure Network Settings (Opening Ports)

In the "Network settings" section:

1. Click "Edit" (top right of the Network settings box)

2. **Firewall (security groups)**: Select "Create security group"

3. **Security group name**: `sentiment-analyzer-sg` (or your choice)

4. **Description**: `Security group for sentiment analyzer app`

5. **Inbound security group rules**: You'll see SSH rule already there. Now add more:

### Rule 1 (Already there):
- **Type**: SSH
- **Protocol**: TCP
- **Port range**: 22
- **Source type**: My IP (RECOMMENDED for security)
  - This restricts SSH access to only your current IP address
- **Description**: SSH access

### Rule 2 (Click "Add security group rule"):
- **Type**: Custom TCP
- **Protocol**: TCP
- **Port range**: 8501
- **Source type**: Anywhere-IPv4 (0.0.0.0/0)
  - This allows anyone to access your Streamlit app
- **Description**: Streamlit app access

### Optional Rule 3 (if using nginx later):
- Click "Add security group rule"
- **Type**: HTTP
- **Protocol**: TCP
- **Port range**: 80
- **Source type**: Anywhere-IPv4 (0.0.0.0/0)
- **Description**: HTTP access

Your rules should look like this:
```
Type          Protocol  Port Range  Source
----          --------  ----------  ------
SSH           TCP       22          My IP
Custom TCP    TCP       8501        0.0.0.0/0
HTTP          TCP       80          0.0.0.0/0 (optional)
```

## Step 8: Configure Storage

In the "Configure storage" section:

1. **Size (GiB)**: Change from 8 to **20 GB**
   - The model training needs space
   - 20 GB is enough and still cheap (~$2/month)
2. **Volume Type**: gp3 (default is fine)
3. Leave other settings as default

## Step 9: Review and Launch

1. On the right side, you'll see a "Summary" panel showing:
   - Number of instances: 1
   - Instance type: t2.small
   - Estimated cost

2. Review everything one more time

3. Click the orange **"Launch instance"** button at the bottom right

4. You'll see a success message!

## Step 10: Wait for Instance to Start

1. Click "View all instances" or go to EC2 Dashboard > Instances

2. You'll see your instance with:
   - **Instance state**: First "Pending" (yellow), then "Running" (green)
   - Wait until it shows **"Running"** (takes 1-2 minutes)
   - **Status check**: Wait until it shows "2/2 checks passed" (takes another 1-2 minutes)

3. Once running, you'll see:
   - **Public IPv4 address**: This is the IP you'll use to SSH and access your app
   - Example: `3.84.123.45`

## Step 11: Prepare Your SSH Key (Mac/Linux)

Before connecting, set the correct permissions on your key file:

```bash
# Move key to .ssh folder (recommended)
mv ~/Downloads/my-ec2-key.pem ~/.ssh/

# Set correct permissions (required by SSH)
chmod 400 ~/.ssh/my-ec2-key.pem
```

## Step 12: Connect to Your Instance

### Option A: Using Terminal (Mac/Linux)

```bash
ssh -i ~/.ssh/my-ec2-key.pem ubuntu@YOUR_PUBLIC_IP
```

Replace `YOUR_PUBLIC_IP` with the actual IP from Step 10.

Example:
```bash
ssh -i ~/.ssh/my-ec2-key.pem ubuntu@3.84.123.45
```

**First time connecting**: You'll see a message asking "Are you sure you want to continue connecting?" - Type `yes` and press Enter.

### Option B: Using EC2 Instance Connect (Browser-based)

1. In EC2 Console, select your instance
2. Click "Connect" button at the top
3. Choose "EC2 Instance Connect" tab
4. Click "Connect" button
5. A browser terminal will open

### Option C: Windows (PuTTY)

If you're on Windows and downloaded a .ppk file:
1. Open PuTTY
2. **Host Name**: ubuntu@YOUR_PUBLIC_IP
3. Connection > SSH > Auth > Credentials: Browse and select your .ppk file
4. Click "Open"

## Step 13: Verify Connection

Once connected, you should see something like:
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.2.0-1009-aws x86_64)
...
ubuntu@ip-172-31-xx-xx:~$
```

You're now connected to your EC2 instance! 🎉

## Next Steps

Now you can proceed with the deployment:

1. **Push your code to GitHub** (if not already):
   ```bash
   # On your local machine
   cd /Users/ayaan/Documents/GitHub/cs484project
   git add .
   git commit -m "Add deployment files"
   git push
   ```

2. **Run the setup script on EC2**:
   ```bash
   # On your EC2 instance
   wget https://raw.githubusercontent.com/YOUR_USERNAME/cs484project/main/setup_ec2.sh
   chmod +x setup_ec2.sh
   ./setup_ec2.sh
   ```

3. **Access your app**:
   - Open browser: `http://YOUR_PUBLIC_IP:8501`

## Troubleshooting

### Can't connect via SSH?
- Check security group has port 22 open for your IP
- Verify you're using the correct key file
- Make sure key has correct permissions: `chmod 400 key.pem`
- Check you're using `ubuntu@` not `ec2-user@`

### Forgot to open port 8501?
1. Go to EC2 Console > Instances
2. Click your instance
3. Click "Security" tab
4. Click the security group link
5. Click "Edit inbound rules"
6. Add the missing rule for port 8501
7. Save rules

### Lost your key pair?
- Unfortunately, you cannot recover it
- You'll need to create a new instance with a new key pair

### Want to stop/start instance to save money?
- **Stop**: EC2 Console > Select instance > Instance state > Stop instance
  - No compute charges while stopped (only storage ~$2/month)
  - Public IP will change when you restart (use Elastic IP to keep it)
- **Start**: Instance state > Start instance

## Cost Management

### See current costs:
1. AWS Console > Billing Dashboard
2. Click "Bills" to see detailed breakdown

### Set up billing alerts:
1. Billing Dashboard > Billing preferences
2. Enable "Receive Billing Alerts"
3. Set up CloudWatch alarm for spending threshold

### Free Tier Note:
- First 750 hours/month of t2.micro is free (first 12 months)
- t2.small is NOT free tier - you'll be charged from day 1

## Important Notes

- **Keep your .pem key safe** - it's like your password!
- **Write down your Public IP** - you'll need it
- **Instance will keep running until you stop it** - This means charges will accumulate
- **To save money**: Stop the instance when not using it
