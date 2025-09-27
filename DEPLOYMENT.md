# 🚀 GitHub Deployment Guide

## Complete Setup Instructions

### Prerequisites
- GitHub account
- Gmail account with 2FA enabled
- Basic understanding of GitHub Actions

---

## Step-by-Step Deployment

### 1. Repository Setup
```bash
# Create new repository on GitHub (public or private)
# Repository name: multi-archetype-scanner
# Initialize with README: NO (we'll provide our own)

# Clone to local machine
git clone https://github.com/YOUR_USERNAME/multi-archetype-scanner.git
cd multi-archetype-scanner
```

### 2. File Upload
Copy these files to your repository:
- `scanner.py` - Main scanner application
- `daily-scanner.yml` - GitHub Actions workflow (place in `.github/workflows/`)
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `.gitignore` - Git ignore rules

### 3. Create Directory Structure
```bash
# Create GitHub Actions directory
mkdir -p .github/workflows
mv daily-scanner.yml .github/workflows/
```

### 4. Gmail App Password Setup
1. **Go to Gmail Settings**
   - Visit: https://myaccount.google.com/security
   
2. **Enable 2-Factor Authentication**
   - Click "2-Step Verification"
   - Follow setup instructions
   
3. **Generate App Password**
   - Click "App Passwords"
   - Select "Mail" from dropdown
   - Click "Generate"
   - **Save the 16-character password** (you'll need this for GitHub)

### 5. GitHub Secrets Configuration
1. **Navigate to Repository Settings**
   - Go to your repository on GitHub
   - Click "Settings" tab
   - Click "Secrets and Variables" → "Actions"

2. **Add Required Secrets**
   - Click "New repository secret"
   - Add these two secrets:
   
   **SECRET 1:**
   - Name: `EMAIL_FROM`
   - Value: `paras.m.parmar@gmail.com`
   
   **SECRET 2:**
   - Name: `EMAIL_PASSWORD`
   - Value: `[Your 16-character Gmail App Password]`

### 6. Commit and Push Files
```bash
git add .
git commit -m "Initial deployment: Multi-Archetype Trading Scanner

- Added main scanner with 4 trading strategies
- GitHub Actions workflow for daily 10 AM IST execution
- Comprehensive email reporting system
- Chartink integration for Indian stocks
- Professional HTML email formatting"

git push origin main
```

### 7. Test the Deployment
1. **Manual Test Run**
   - Go to "Actions" tab in your GitHub repository
   - Click "Multi-Archetype Trading Scanner"
   - Click "Run workflow" button
   - Select "main" branch
   - Click "Run workflow"

2. **Monitor Execution**
   - Watch the workflow run in real-time
   - Check for any errors in the logs
   - Verify email delivery to `paras.m.parmar@gmail.com`

3. **Verify Email Content**
   - Check inbox (and spam folder)
   - Confirm HTML formatting is correct
   - Verify stock data is populated

---

## Automated Schedule

### Default Schedule
- **Frequency**: Every weekday (Monday-Friday)
- **Time**: 10:00 AM IST (4:30 AM UTC)
- **Duration**: 2-3 minutes per execution
- **Next Run**: Shown in GitHub Actions tab

### Schedule Customization
To change the time, edit `.github/workflows/daily-scanner.yml`:

```yaml
schedule:
  - cron: '30 4 * * 1-5'  # Current: 10:00 AM IST
  # Examples:
  # - cron: '0 5 * * 1-5'   # 10:30 AM IST  
  # - cron: '30 3 * * 1-5'  # 9:00 AM IST
  # - cron: '0 6 * * 1-5'   # 11:30 AM IST
```

---

## Verification Checklist

### ✅ Pre-Deployment
- [ ] GitHub repository created
- [ ] All files uploaded correctly
- [ ] Directory structure matches requirements
- [ ] Gmail 2FA enabled
- [ ] App password generated and saved

### ✅ Configuration
- [ ] EMAIL_FROM secret added to GitHub
- [ ] EMAIL_PASSWORD secret added to GitHub
- [ ] Secrets are accessible in Actions
- [ ] No syntax errors in workflow file

### ✅ Testing
- [ ] Manual workflow run successful
- [ ] No errors in GitHub Actions logs
- [ ] Email received at paras.m.parmar@gmail.com
- [ ] Email content displays correctly
- [ ] Stock data is populated (or sample data shown)

### ✅ Production Ready
- [ ] Automatic schedule is active
- [ ] Next run time is displayed
- [ ] Error handling working properly
- [ ] Rate limiting respected
- [ ] Performance metrics logged

---

## Monitoring and Maintenance

### Daily Monitoring
- Check GitHub Actions for successful runs
- Verify email delivery
- Review stock counts and market data

### Weekly Review
- Analyze strategy performance
- Check for any systematic errors
- Review market conditions vs results

### Monthly Maintenance
- Update dependencies if needed
- Review and optimize queries
- Assess strategy effectiveness

---

## Support and Troubleshooting

### Common Issues
1. **Email authentication failure**
   - Verify Gmail App Password is correct
   - Check 2FA is enabled
   - Ensure EMAIL_PASSWORD secret is set

2. **No stocks found**
   - Normal during market holidays
   - Check Chartink.com accessibility
   - Review market conditions

3. **Workflow not running**
   - Verify cron syntax
   - Check GitHub Actions are enabled
   - Review repository permissions

### Getting Help
- Check GitHub Actions logs for detailed errors
- Review README.md for troubleshooting guide
- Verify all setup steps were completed
- Test with manual workflow trigger first

---

## Security Best Practices

### Protecting Credentials
- Never commit email passwords to Git
- Use GitHub Secrets for sensitive data
- Rotate App Passwords periodically
- Monitor for unauthorized access

### Repository Security
- Keep repository private if preferred
- Limit collaborator access
- Review workflow permissions
- Monitor Actions usage

---

## Success Confirmation

### You've Successfully Deployed When:
1. ✅ GitHub Actions shows green checkmark for workflow runs
2. ✅ Daily emails are received at 10:00 AM IST
3. ✅ Email contains properly formatted stock data
4. ✅ Multiple trading strategies show results
5. ✅ No error notifications in GitHub

### Next Steps After Deployment:
1. **Monitor Performance**: Track daily results for pattern analysis
2. **Customize Strategies**: Modify queries based on market conditions
3. **Risk Management**: Use results within proper position sizing framework
4. **Strategy Optimization**: Analyze which archetypes perform best
5. **Continuous Learning**: Study the three foundational trading approaches

---

🎯 **Deployment Complete!** 

Your Multi-Archetype Trading Scanner is now running automatically every weekday, implementing the three foundational trading strategies and delivering insights directly to your inbox.

**Happy Systematic Trading!** 📈