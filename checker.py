import requests
from models import db, ScoreEvent
from config import Config

class URLChecker:
    """Handles URL checking and scoring logic"""
    
    @staticmethod
    def check_application_url(user, app):
        """Check the application URL for the required content"""
        if not user.url:
            return
        
        try:
            response = requests.get(user.url, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                # Check for HTTPS
                if user.url.startswith('https://'):
                    user.score += Config.POINTS_HTTPS
                    URLChecker._add_event(
                        user.id,
                        f"Application URL using HTTPS (+{Config.POINTS_HTTPS})",
                        Config.POINTS_HTTPS
                    )
                    print(f"✓ User {user.username} - HTTPS bonus! Total: {user.score}")
                
                # Check for CloudFront cache hit
                x_cache_header = response.headers.get('X-Cache', '')
                if 'Hit from cloudfront' in x_cache_header:
                    user.score += Config.POINTS_CLOUDFRONT
                    URLChecker._add_event(
                        user.id,
                        f"CloudFront cache hit detected (+{Config.POINTS_CLOUDFRONT})",
                        Config.POINTS_CLOUDFRONT
                    )
                    print(f"✓ User {user.username} - CloudFront cache hit! Total: {user.score}")
                
                # Check for required content
                if Config.APP_URL_REQUIRED_TEXT in response.text:
                    user.score += Config.POINTS_PER_CHECK
                    URLChecker._add_event(
                        user.id, 
                        f"Application URL is valid (+{Config.POINTS_PER_CHECK})", 
                        Config.POINTS_PER_CHECK
                    )
                    print(f"✓ User {user.username} - App URL scored! Total: {user.score}")
                else:
                    URLChecker._add_event(
                        user.id,
                        "Application URL returned 200 but missing required content (+0)",
                        0
                    )
            else:
                URLChecker._add_event(
                    user.id,
                    f"Application URL returned status {response.status_code} (+0)",
                    0
                )
        except Exception as e:
            URLChecker._add_event(
                user.id,
                f"Application URL error: {str(e)[:100]} (+0)",
                0
            )
            print(f"✗ Error checking app URL for {user.username}: {e}")
    
    @staticmethod
    def check_api_url(user, app):
        """Check the API Gateway URL for the required JSON response"""
        if not user.api_url:
            return
        
        try:
            response = requests.get(user.api_url, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("account_id") == user.aws_account_id:
                        user.score += Config.POINTS_PER_CHECK
                        URLChecker._add_event(
                            user.id,
                            f"API URL is valid (+{Config.POINTS_PER_CHECK})",
                            Config.POINTS_PER_CHECK
                        )
                        print(f"✓ User {user.username} - API URL scored! Total: {user.score}")
                    else:
                        URLChecker._add_event(
                            user.id,
                            "API URL returned 200 but invalid account_id (+0)",
                            0
                        )
                except ValueError:
                    URLChecker._add_event(
                        user.id,
                        "API URL returned 200 but response is not valid JSON (+0)",
                        0
                    )
            else:
                URLChecker._add_event(
                    user.id,
                    f"API URL returned status {response.status_code} (+0)",
                    0
                )
        except Exception as e:
            URLChecker._add_event(
                user.id,
                f"API URL error: {str(e)[:100]} (+0)",
                0
            )
            print(f"✗ Error checking API URL for {user.username}: {e}")
    
    @staticmethod
    def _add_event(user_id, reason, points):
        """Helper method to add a score event"""
        event = ScoreEvent(user_id=user_id, reason=reason, points=points)
        db.session.add(event)
