#!/bin/bash

# RakanGPT - Deploy to Heroku
# Prerequisites: Heroku CLI installed and logged in

set -e

echo "╔═══════════════════════════════════════╗"
echo "║  RakanGPT - Heroku Deployment Setup   ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not installed"
    echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✓ Heroku CLI found"
echo ""

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "⚠️  Not logged in to Heroku"
    echo "Running: heroku login"
    heroku login
fi

echo ""
echo "Creating Heroku app..."
read -p "Enter app name (e.g., my-rakangpt): " APP_NAME

if heroku create "$APP_NAME" 2>/dev/null; then
    echo "✓ App created: $APP_NAME"
else
    echo "❌ Failed to create app (may already exist)"
    exit 1
fi

echo ""
echo "Setting environment variables..."
read -sp "Enter your ANTHROPIC_API_KEY: " API_KEY
echo ""

heroku config:set ANTHROPIC_API_KEY="$API_KEY" --app="$APP_NAME"
echo "✓ API key configured"

echo ""
echo "Deploying application..."
git push heroku main 2>/dev/null || {
    echo "❌ Deployment failed"
    echo "Make sure you're in the git repository and have main branch"
    exit 1
}

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║      Deployment Complete! 🎉          ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "Your app is live at:"
echo "https://${APP_NAME}.herokuapp.com"
echo ""
echo "Opening app in browser..."
heroku open --app="$APP_NAME"
