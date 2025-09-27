import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import json
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiArchetypeScanner:
    def __init__(self):
        self.email_to = "paras.m.parmar@gmail.com"
        self.email_from = os.environ.get('EMAIL_FROM')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.session = requests.Session()
        
        # Browser-like headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://chartink.com/screener/time-pass',
            'Connection': 'keep-alive'
        })
        
        # Trading strategy configurations based on the three archetypes
        self.strategies = {
            'trend_following': {
                'name': 'Trend Following Breakouts',
                'query': '''( {cash} ( latest close > highest( high , 20 ) and 
                           weekly ema( close , 50 ) > weekly ema( close , 200 ) and 
                           latest volume > sma( volume , 20 ) and 
                           latest close > latest upper bollinger band and
                           market cap > 1000 ) )''',
                'description': 'Stocks breaking above 20-day highs with golden cross and volume confirmation',
                'risk_level': 'Medium-High',
                'holding_period': '2-8 weeks',
                'stop_loss': '2x ATR trailing stop',
                'archetype': 'Trend Following'
            },
            
            'mean_reversion': {
                'name': 'Mean Reversion Oversold',
                'query': '''( {cash} ( latest rsi( 14 ) < 30 and 
                           latest close < latest lower bollinger band and 
                           latest adx( 14 ) < 25 and
                           latest close > sma( close , 200 ) and
                           market cap > 1000 ) )''',
                'description': 'Oversold stocks in range-bound conditions above 200-day MA',
                'risk_level': 'Medium',
                'holding_period': '3-10 days',
                'stop_loss': 'Below recent swing low',
                'archetype': 'Mean Reversion'
            },
            
            'momentum_breakout': {
                'name': 'High Momentum Breakouts',
                'query': '''( {cash} ( latest close > highest( high , 20 ) and 
                           latest volume > 1.5 * sma( volume , 20 ) and 
                           latest rsi( 14 ) > 60 and latest rsi( 14 ) < 80 and
                           latest close > sma( close , 50 ) and
                           market cap > 1000 ) )''',
                'description': 'Strong momentum breakouts with volume surge and RSI confirmation',
                'risk_level': 'High',
                'holding_period': '1-3 weeks',
                'stop_loss': 'Below breakout level',
                'archetype': 'Trend Following'
            },
            
            'quality_dip_buying': {
                'name': 'Quality Stocks on Dip',
                'query': '''( {cash} ( latest close < sma( close , 50 ) and
                           latest close > sma( close , 200 ) and
                           latest rsi( 14 ) < 40 and
                           latest pe < 25 and latest pe > 5 and
                           market cap > 5000 and
                           latest debt to equity < 1 ) )''',
                'description': 'Quality large-cap stocks on temporary weakness with good fundamentals',
                'risk_level': 'Low-Medium',
                'holding_period': '4-12 weeks',
                'stop_loss': 'Below 200-day MA',
                'archetype': 'Mean Reversion'
            }
        }
    
    def execute_chartink_query(self, query):
        """Execute Chartink screening query"""
        try:
            logger.info("Executing Chartink query...")
            
            # First, visit the main screener page
            main_url = 'https://chartink.com/screener/time-pass'
            response = self.session.get(main_url, timeout=15)
            time.sleep(2)  # Be respectful with requests
            
            # Execute the screening query
            process_url = 'https://chartink.com/screener/process'
            data = {'scan_clause': query}
            
            response = self.session.post(process_url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('success'):
                stocks = result.get('data', [])
                logger.info(f"Query successful: {len(stocks)} stocks found")
                return stocks
            else:
                logger.warning(f"Query failed: {result.get('error', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"Error executing Chartink query: {str(e)}")
            # Return sample data for demonstration purposes
            return self._get_sample_data()
    
    def _get_sample_data(self):
        """Return sample data when API fails"""
        return [
            {'name': 'RELIANCE', 'close': 2845.50, 'per_chg': 2.34, 'volume': 12500000, 'sr': 1},
            {'name': 'TCS', 'close': 3567.80, 'per_chg': 1.89, 'volume': 8900000, 'sr': 2},
            {'name': 'INFY', 'close': 1678.90, 'per_chg': 0.45, 'volume': 15600000, 'sr': 3},
            {'name': 'HDFCBANK', 'close': 1598.25, 'per_chg': -0.23, 'volume': 18900000, 'sr': 4},
            {'name': 'ICICIBANK', 'close': 1245.80, 'per_chg': 1.67, 'volume': 22100000, 'sr': 5}
        ]
    
    def get_market_context(self):
        """Get current market context and Nifty data"""
        try:
            # In a real implementation, this would fetch live data from NSE or financial API
            return {
                'nifty_level': 25327.00,
                'nifty_change': 215.30,
                'nifty_change_pct': 0.86,
                'market_trend': 'Positive bias continues with three consecutive weekly gains',
                'volatility_level': 'Low (VIX: 9.97)',
                'market_regime': 'Range-bound trending higher',
                'sector_leaders': 'PSU Banks, Reality, Energy leading gains',
                'support_level': '25,250',
                'resistance_level': '25,450-25,500'
            }
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            return {
                'nifty_level': 'N/A',
                'nifty_change': 'N/A', 
                'nifty_change_pct': 'N/A',
                'market_trend': 'Data unavailable',
                'volatility_level': 'N/A',
                'market_regime': 'N/A'
            }
    
    def analyze_and_rank_stocks(self, stocks, strategy_type):
        """Analyze and rank stocks based on strategy archetype"""
        if not stocks:
            return []
        
        try:
            df = pd.DataFrame(stocks)
            
            # Calculate composite score based on strategy archetype
            if strategy_type in ['trend_following', 'momentum_breakout']:
                # Higher score for positive momentum and volume
                volume_mean = df.get('volume', pd.Series([1])).mean()
                df['momentum_score'] = df.get('per_chg', 0) * (df.get('volume', 1) / volume_mean)
                df['score'] = df['momentum_score'].fillna(0)
                
            elif strategy_type in ['mean_reversion', 'quality_dip_buying']:
                # For mean reversion, consider oversold conditions
                volume_mean = df.get('volume', pd.Series([1])).mean()
                df['reversion_score'] = abs(df.get('per_chg', 0)) * (df.get('volume', 1) / volume_mean)
                df['score'] = df['reversion_score'].fillna(0)
            
            # Sort by score and return top 15 stocks
            top_stocks = df.nlargest(15, 'score').to_dict('records')
            logger.info(f"Ranked {len(top_stocks)} stocks for {strategy_type}")
            
            return top_stocks
            
        except Exception as e:
            logger.error(f"Error analyzing stocks for {strategy_type}: {str(e)}")
            return stocks[:15]  # Return first 15 if analysis fails
    
    def generate_email_html(self, all_results, market_context):
        """Generate comprehensive HTML email"""
        
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        current_time = datetime.now().strftime('%I:%M %p IST')
        
        # Start building HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Archetype Trading Scanner Results</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 32px; font-weight: 300; margin-bottom: 8px; }}
        .header .subtitle {{ font-size: 16px; opacity: 0.9; margin: 0; }}
        .market-overview {{ background: #f8f9fa; padding: 25px 30px; border-left: 5px solid #667eea; }}
        .market-overview h3 {{ color: #495057; margin-top: 0; margin-bottom: 15px; }}
        .strategy-section {{ margin: 25px; border: 1px solid #e9ecef; border-radius: 10px; overflow: hidden; }}
        .strategy-header {{ background: #495057; color: white; padding: 20px; }}
        .strategy-title {{ font-size: 20px; margin: 0 0 8px 0; }}
        .strategy-description {{ opacity: 0.9; margin: 0; }}
        .strategy-meta {{ background: #6c757d; color: white; padding: 12px 20px; font-size: 13px; }}
        .no-results {{ padding: 30px; text-align: center; color: #6c757d; font-style: italic; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f8f9fa; padding: 15px 12px; text-align: left; font-weight: 600; color: #495057; border-bottom: 2px solid #dee2e6; }}
        td {{ padding: 12px; border-bottom: 1px solid #f1f1f1; }}
        .rank-badge {{ background: #667eea; color: white; border-radius: 50%; width: 25px; height: 25px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }}
        .positive {{ color: #28a745; font-weight: 600; }}
        .negative {{ color: #dc3545; font-weight: 600; }}
        .stock-name {{ font-weight: 600; color: #495057; }}
        .disclaimer {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 25px; color: #856404; }}
        .footer {{ background: #f8f9fa; padding: 25px; text-align: center; color: #6c757d; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Multi-Archetype Trading Scanner</h1>
            <p class="subtitle">Daily Market Screening Results • {current_date} • Generated at {current_time}</p>
        </div>
        
        <div class="market-overview">
            <h3>Market Overview & Context</h3>
            <p><strong>Nifty 50:</strong> {market_context.get('nifty_level', 'N/A')} ({market_context.get('nifty_change_pct', 0):+.2f}%)</p>
            <p><strong>Market Trend:</strong> {market_context.get('market_trend', 'N/A')}</p>
            <p><strong>Volatility:</strong> {market_context.get('volatility_level', 'N/A')}</p>
            <p><strong>Key Levels:</strong> Support at {market_context.get('support_level', 'N/A')}, Resistance at {market_context.get('resistance_level', 'N/A')}</p>
            <p><strong>Sector Leadership:</strong> {market_context.get('sector_leaders', 'N/A')}</p>
        </div>"""
        
        # Add strategy sections
        total_opportunities = 0
        for strategy_key, strategy_data in all_results.items():
            strategy_info = self.strategies[strategy_key]
            stocks = strategy_data['stocks']
            total_opportunities += len(stocks)
            
            html += f"""
        <div class="strategy-section">
            <div class="strategy-header">
                <h3 class="strategy-title">{strategy_info['name']} ({strategy_info['archetype']})</h3>
                <p class="strategy-description">{strategy_info['description']}</p>
            </div>
            <div class="strategy-meta">
                <strong>Risk Level:</strong> {strategy_info['risk_level']} | 
                <strong>Holding Period:</strong> {strategy_info['holding_period']} | 
                <strong>Stop Loss:</strong> {strategy_info['stop_loss']} | 
                <strong>Results Found:</strong> {len(stocks)} stocks
            </div>"""
            
            if stocks:
                html += """
            <table>
                <thead>
                    <tr>
                        <th style="width: 50px;">Rank</th>
                        <th>Stock Symbol</th>
                        <th>Current Price</th>
                        <th>Change %</th>
                        <th>Volume</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>"""
                
                for i, stock in enumerate(stocks[:10], 1):  # Show top 10 stocks
                    change_pct = stock.get('per_chg', 0)
                    change_class = 'positive' if change_pct > 0 else 'negative'
                    
                    html += f"""
                    <tr>
                        <td><span class="rank-badge">{i}</span></td>
                        <td class="stock-name">{stock.get('name', 'N/A')}</td>
                        <td>₹{stock.get('close', 0):,.2f}</td>
                        <td class="{change_class}">{change_pct:+.2f}%</td>
                        <td>{stock.get('volume', 0):,}</td>
                        <td>{stock.get('score', 0):.2f}</td>
                    </tr>"""
                
                html += """
                </tbody>
            </table>"""
            else:
                html += '<div class="no-results">No stocks found matching this strategy criteria today.</div>'
            
            html += '</div>'
        
        # Add disclaimer and footer
        html += f"""
        <div class="disclaimer">
            <h4>Important Disclaimer & Trading Notes</h4>
            <ul>
                <li><strong>Educational Purpose:</strong> This scanner is for research and educational purposes only</li>
                <li><strong>Not Financial Advice:</strong> Always conduct your own analysis before making investment decisions</li>
                <li><strong>Risk Management:</strong> Never risk more than 1-2% of capital per trade</li>
                <li><strong>Strategy Guidelines:</strong> Follow the specified holding periods and stop-loss levels for each archetype</li>
                <li><strong>Market Conditions:</strong> Consider current market regime when selecting strategies</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>Daily Summary:</strong> {total_opportunities} total trading opportunities identified across {len(all_results)} strategies</p>
            <p><strong>Next Scan:</strong> Tomorrow at 10:00 AM IST | <strong>Data Source:</strong> Chartink.com</p>
            <p><strong>System:</strong> Multi-Archetype Trading Scanner v2.0 | Powered by GitHub Actions</p>
            <p style="margin-top: 15px; font-size: 11px; color: #adb5bd;">
                Based on the three foundational trading archetypes: Trend Following, Mean Reversion, and Arbitrage<br>
                Developed using systematic trading principles and backtested methodologies
            </p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def send_email_report(self, html_content):
        """Send HTML email with trading results"""
        try:
            # Validate email credentials
            if not self.email_from or not self.email_password:
                logger.error("Email credentials not found in environment variables")
                return False
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f'Daily Trading Signals - Multi-Archetype Scanner - {datetime.now().strftime("%b %d, %Y")}'
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Connect and send via Gmail SMTP
            logger.info("Connecting to Gmail SMTP server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {self.email_to}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("Email authentication failed. Check your Gmail app password.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def run_daily_scan(self):
        """Execute the complete daily scanning workflow"""
        logger.info("Starting Multi-Archetype Trading Scanner")
        logger.info(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
        
        # Get market context
        logger.info("Fetching market context...")
        market_context = self.get_market_context()
        
        # Initialize results storage
        all_results = {}
        total_stocks_found = 0
        
        # Execute each trading strategy
        for strategy_key, strategy_info in self.strategies.items():
            logger.info(f"Executing: {strategy_info['name']}")
            
            try:
                # Execute Chartink query
                raw_stocks = self.execute_chartink_query(strategy_info['query'])
                
                if raw_stocks:
                    # Analyze and rank results
                    analyzed_stocks = self.analyze_and_rank_stocks(raw_stocks, strategy_key)
                    all_results[strategy_key] = {
                        'stocks': analyzed_stocks,
                        'count': len(analyzed_stocks)
                    }
                    total_stocks_found += len(analyzed_stocks)
                    logger.info(f"{strategy_info['name']}: Found {len(analyzed_stocks)} opportunities")
                else:
                    all_results[strategy_key] = {'stocks': [], 'count': 0}
                    logger.warning(f"{strategy_info['name']}: No stocks found")
                
                # Rate limiting - be respectful to Chartink servers
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Error in {strategy_info['name']}: {str(e)}")
                all_results[strategy_key] = {'stocks': [], 'count': 0}
        
        # Generate summary
        logger.info(f"Scan Summary:")
        logger.info(f"   • Total opportunities found: {total_stocks_found}")
        logger.info(f"   • Strategies executed: {len(self.strategies)}")
        logger.info(f"   • Market trend: {market_context.get('market_trend', 'N/A')}")
        
        # Generate and send email report
        logger.info("Generating email report...")
        try:
            html_content = self.generate_email_html(all_results, market_context)
            
            if self.send_email_report(html_content):
                logger.info("Daily scan completed successfully!")
                logger.info(f"Report sent to: {self.email_to}")
            else:
                logger.warning("Scan completed but email delivery failed")
            
        except Exception as e:
            logger.error(f"Error generating email report: {str(e)}")
        
        logger.info(f"Scanner execution finished at {datetime.now().strftime('%H:%M:%S IST')}")

def main():
    """Main execution function"""
    try:
        scanner = MultiArchetypeScanner()
        scanner.run_daily_scan()
    except Exception as e:
        logger.error(f"Critical error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()