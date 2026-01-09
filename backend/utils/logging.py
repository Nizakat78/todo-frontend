import logging
from datetime import datetime
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLogger:
    """Logger for security events and errors"""

    @staticmethod
    def log_security_event(event_type: str, user_id: str = None, ip_address: str = None, details: Dict[str, Any] = None):
        """Log security-related events"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details or {}
        }

        logger.info(f"SECURITY_EVENT: {json.dumps(log_data)}")

    @staticmethod
    def log_auth_failure(user_id: str = None, ip_address: str = None, reason: str = None):
        """Log authentication failures"""
        SecurityLogger.log_security_event(
            event_type="AUTH_FAILURE",
            user_id=user_id,
            ip_address=ip_address,
            details={"reason": reason}
        )

    @staticmethod
    def log_unauthorized_access(user_id: str, requested_resource: str, ip_address: str = None):
        """Log unauthorized access attempts"""
        SecurityLogger.log_security_event(
            event_type="UNAUTHORIZED_ACCESS",
            user_id=user_id,
            ip_address=ip_address,
            details={"requested_resource": requested_resource}
        )

    @staticmethod
    def log_user_registration(user_id: str, ip_address: str = None):
        """Log user registration events"""
        SecurityLogger.log_security_event(
            event_type="USER_REGISTRATION",
            user_id=user_id,
            ip_address=ip_address,
            details={}
        )

    @staticmethod
    def log_successful_login(user_id: str, ip_address: str = None):
        """Log successful login events"""
        SecurityLogger.log_security_event(
            event_type="SUCCESSFUL_LOGIN",
            user_id=user_id,
            ip_address=ip_address,
            details={}
        )

    @staticmethod
    def log_failed_login_attempt(email: str, ip_address: str = None):
        """Log failed login attempt events"""
        SecurityLogger.log_security_event(
            event_type="FAILED_LOGIN_ATTEMPT",
            user_id=email,  # Using email as identifier for failed attempts
            ip_address=ip_address,
            details={}
        )

    @staticmethod
    def log_logout(user_id: str, ip_address: str = None):
        """Log logout events"""
        SecurityLogger.log_security_event(
            event_type="LOGOUT",
            user_id=user_id,
            ip_address=ip_address,
            details={}
        )

# Standard logger for general application events
def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # Prevent adding multiple handlers if already configured
    if not log.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log