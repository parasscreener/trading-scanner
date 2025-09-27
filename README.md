# 📊 Multi-Archetype Trading Scanner

**Automated daily stock screening system implementing three foundational trading strategies for Indian equity markets. Runs every weekday at 10:00 AM IST and delivers insights via email.**

## 🎯 Strategy Overview

This scanner implements the three foundational trading archetypes identified by systematic traders:

### 1. **Trend Following** 📈
- **Principle**: Cut losses short, let profits run
- **Signals**: 20-day breakouts + golden cross + volume confirmation
- **Win Rate**: 30-40% (small losses, big wins)
- **Holding Period**: 2-8 weeks
- **Best Markets**: Trending, volatile periods

### 2. **Mean Reversion** 🔄  
- **Principle**: Buy low, sell high within ranges
- **Signals**: RSI < 30 + Bollinger Band oversold + ADX < 25
- **Win Rate**: 60-70% (many small wins)
- **Holding Period**: 3-10 days
- **Best Markets**: Range-bound, sideways markets

### 3. **High Momentum Breakouts** 🚀
- **Principle**: Capture strong momentum with volume confirmation  
- **Signals**: 20-day breakouts + 1.5x volume + RSI 60-80
- **Win Rate**: 45-55% (balanced approach)
- **Holding Period**: 1-3 weeks
- **Best Markets**: Strong trending phases

### 4. **Quality Dip Buying** 💎
- **Principle**: Quality large-caps on temporary weakness
- **Signals**: Below 50 EMA + above 200 EMA + low PE + good fundamentals
- **Win Rate**: 55-65% (conservative approach)
- **Holding Period**: 4-12 weeks
- **Best Markets**: Market corrections in bull trends

## 🚀 Quick Setup Guide

### Step 1: Create GitHub Repository
```bash
# Create new repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/multi-archetype-scanner.git
cd multi-archetype-scanner

# Copy all files from this package
# Commit and push
git add .
git commit -m "Initial setup: Multi-Archetype Trading Scanner"
git push origin main
```

### Step 2: Configure Secrets
Go to **Repository Settings → Secrets and Variables → Actions**

Add these required secrets:
- **EMAIL_FROM**: `paras.m.parmar@gmail.com` (your Gmail address)
- **EMAIL_PASSWORD**: Your Gmail App Password (see setup below)

### Step 3: Gmail App Password Setup
1. **Enable 2FA** on your Gmail account
2. Go to **Google Account → Security → App Passwords**
3. **Generate password** for "Mail" application
4. **Copy the 16-character password** and use it in GitHub secrets
5. ⚠️ **Never use your regular Gmail password**

### Step 4: Test Deployment
1. Go to **Actions** tab in your GitHub repository
2. Click **Multi-Archetype Trading Scanner**
3. Click **Run workflow** to test manually
4. Check logs for successful execution
5. Verify email delivery to `paras.m.parmar@gmail.com`

## ⏰ Automated Schedule

- **When**: Every weekday at **10:00 AM IST** (4:30 AM UTC)
- **Duration**: Approximately 2-3 minutes per run
- **Weekend**: Automatically skipped (Saturday/Sunday)
- **Holidays**: Runs but handles market closures gracefully
- **Manual Trigger**: Available for testing anytime

## 📧 Email Report Features

### Professional HTML Format
- **Market Overview**: Nifty level, trend direction, volatility
- **Strategy Results**: Top 10-12 stocks per strategy
- **Risk Metrics**: Individual risk levels and holding periods
- **Mobile Responsive**: Optimized for all devices
- **Color Coding**: Green/red for positive/negative changes

### Content Includes
- **Stock Rankings**: Sorted by composite score
- **Current Prices**: Real-time price data
- **Volume Analysis**: Volume vs. average comparison
- **Technical Levels**: Support/resistance information
- **Risk Guidelines**: Stop-loss and position sizing advice

## 🔍 Chartink Queries Implementation

### Trend Following Query
```
( {cash} ( 
    latest close > highest( high , 20 ) and 
    weekly ema( close , 50 ) > weekly ema( close , 200 ) and 
    latest volume > sma( volume , 20 ) and 
    latest close > latest upper bollinger band and
    market cap > 1000 
) )
```

### Mean Reversion Query
```
( {cash} ( 
    latest rsi( 14 ) < 30 and 
    latest close < latest lower bollinger band and 
    latest adx( 14 ) < 25 and
    latest close > sma( close , 200 ) and
    market cap > 1000 
) )
```

### High Momentum Query
```
( {cash} ( 
    latest close > highest( high , 20 ) and 
    latest volume > 1.5 * sma( volume , 20 ) and 
    latest rsi( 14 ) > 60 and latest rsi( 14 ) < 80 and
    latest close > sma( close , 50 ) and
    market cap > 1000 
) )
```

### Quality Dip Query
```
( {cash} ( 
    latest close < sma( close , 50 ) and
    latest close > sma( close , 200 ) and
    latest rsi( 14 ) < 40 and
    latest pe < 25 and latest pe > 5 and
    market cap > 5000 and
    latest debt to equity < 1 
) )
```

## 🛠️ Technical Architecture

### Core Components
- **Scanner Engine**: Python-based Chartink integration
- **Email System**: SMTP via Gmail with HTML formatting
- **Automation**: GitHub Actions with cron scheduling
- **Error Handling**: Comprehensive logging and fallback mechanisms
- **Rate Limiting**: Respectful API usage with delays

### Dependencies
- **requests**: HTTP client for Chartink API
- **pandas**: Data analysis and ranking
- **smtplib**: Email delivery system
- **logging**: Comprehensive error tracking

### File Structure
```
multi-archetype-scanner/
├── scanner.py                 # Main scanner logic
├── .github/
│   └── workflows/
│       └── daily-scanner.yml  # GitHub Actions workflow
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
└── .gitignore                # Git ignore rules
```

## 🔧 Customization Options

### Change Email Recipient
Edit `scanner.py` line 15:
```python
self.email_to = "your-new-email@gmail.com"
```

### Modify Schedule
Edit `.github/workflows/daily-scanner.yml` cron:
```yaml
schedule:
  - cron: '30 4 * * 1-5'  # Current: 10:00 AM IST weekdays
  # Examples:
  # - cron: '0 5 * * 1-5'   # 10:30 AM IST
  # - cron: '30 3 * * 1-5'  # 9:00 AM IST
```

### Add New Strategy
Edit `scanner.py` and add to `self.strategies`:
```python
'your_strategy': {
    'name': 'Your Strategy Name',
    'query': '''your chartink query here''',
    'description': 'Strategy description',
    'risk_level': 'Medium',
    'holding_period': '1-2 weeks',
    'archetype': 'Trend Following'  # or Mean Reversion
}
```

### Adjust Stock Count
Edit `scanner.py` line in `generate_email_html`:
```python
for i, stock in enumerate(stocks[:10], 1):  # Change 10 to desired count
```

## 📊 Performance Monitoring

### GitHub Actions Logs
- **Execution Status**: Success/failure for each run
- **Stock Counts**: Number of opportunities found per strategy
- **Email Status**: Delivery confirmation
- **Error Details**: Comprehensive error logging

### Email Tracking
- **Delivery Confirmation**: Success message in logs
- **Content Verification**: Check email formatting and data
- **Failure Alerts**: Error notifications in GitHub Actions

## ⚠️ Troubleshooting

### Common Issues

**1. Email Not Sending**
- ✅ Check Gmail 2FA is enabled
- ✅ Verify App Password (not regular password)
- ✅ Confirm EMAIL_FROM and EMAIL_PASSWORD secrets
- ✅ Check spam folder

**2. No Scanner Results**  
- ✅ Verify market hours (scanner runs at 10 AM IST)
- ✅ Check Chartink.com accessibility
- ✅ Review GitHub Actions logs for errors
- ✅ Consider market holidays/weekends

**3. Workflow Not Running**
- ✅ Verify cron syntax in workflow file
- ✅ Check GitHub Actions are enabled
- ✅ Confirm repository is not archived
- ✅ Review GitHub Actions quota

**4. Rate Limiting Issues**
- ✅ Scanner includes 3-second delays between queries
- ✅ Check for excessive manual testing
- ✅ Consider Chartink usage limits

### Debug Mode
Add environment variable for detailed logging:
```yaml
env:
  DEBUG: true
  EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
  EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
```

## 📈 Strategy Performance Notes

### Expected Results
- **Total Opportunities**: 15-50 stocks per day across all strategies
- **Market Dependent**: More opportunities during trending markets
- **Quality Focus**: Minimum market cap filters ensure liquidity
- **Diversified**: Multiple archetypes reduce correlation risk

### Risk Management Guidelines
- **Position Sizing**: Never risk more than 1-2% per trade
- **Stop Losses**: Follow strategy-specific guidelines
- **Diversification**: Don't concentrate in single strategy
- **Market Regime**: Adapt allocation based on conditions

## 🤝 Contributing

### Adding Features
1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-strategy`)
3. Add your improvements
4. Test thoroughly
5. Submit pull request

### Reporting Issues
- Use GitHub Issues for bug reports
- Include error logs and reproduction steps
- Specify environment details (GitHub Actions logs)

## 📄 Legal Disclaimer

**⚠️ IMPORTANT NOTICE**

This tool is provided for **educational and research purposes only**. It is not intended as financial advice or investment recommendations.

- **No Investment Advice**: Results are for informational purposes only
- **Do Your Research**: Always conduct independent analysis
- **Risk Warning**: All trading involves risk of loss
- **No Guarantees**: Past performance doesn't predict future results
- **Professional Advice**: Consult qualified financial advisors

By using this scanner, you acknowledge that:
- You understand the risks involved in trading
- You will not hold the developers liable for any losses
- You will use the information responsibly
- You have read and agree to this disclaimer

## 📞 Support

### Resources
- **Documentation**: This README file
- **GitHub Issues**: Report bugs and feature requests
- **Chartink Help**: https://chartink.com/support
- **GitHub Actions Docs**: https://docs.github.com/en/actions

### Best Practices
- **Test First**: Always run manual workflow before relying on automation
- **Backup Plan**: Have alternative scanning methods
- **Stay Updated**: Monitor for dependency updates
- **Security**: Never share your Gmail App Password

---

**Happy Trading! 📈**

*Built with ❤️ for systematic traders using Python, GitHub Actions, and the three foundational trading archetypes.*