#!/bin/bash
# EC2 Setup Script for Amazon Sentiment Analyzer
# Run this script on your EC2 instance after SSH'ing in

set -e

echo "=========================================="
echo "Setting up Amazon Sentiment Analyzer"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "Installing Python and pip..."
sudo apt install -y python3-pip python3-venv git

# Clone repository (if not already cloned)
if [ ! -d "cs484project" ]; then
    echo "Enter your GitHub repository URL:"
    read REPO_URL
    git clone $REPO_URL cs484project
fi

cd cs484project

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Train the model
echo "Training the sentiment analysis model..."
echo "This may take several minutes..."
python main.py

# Setup systemd service
echo "Setting up systemd service..."
sudo cp streamlit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Your Streamlit app is now running!"
echo "Access it at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8501"
echo ""
echo "Useful commands:"
echo "  - Check status: sudo systemctl status streamlit"
echo "  - View logs: sudo journalctl -u streamlit -f"
echo "  - Restart app: sudo systemctl restart streamlit"
echo "  - Stop app: sudo systemctl stop streamlit"
echo ""
