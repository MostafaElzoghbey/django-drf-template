"""
Throttling classes for the API app.
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class StandardAnonRateThrottle(AnonRateThrottle):
    """
    Throttle for anonymous users.
    """
    
    rate = "100/hour"


class StandardUserRateThrottle(UserRateThrottle):
    """
    Throttle for authenticated users.
    """
    
    rate = "1000/hour"


class BurstAnonRateThrottle(AnonRateThrottle):
    """
    Throttle for anonymous users with a higher burst rate.
    """
    
    scope = "burst_anon"
    rate = "300/minute"


class BurstUserRateThrottle(UserRateThrottle):
    """
    Throttle for authenticated users with a higher burst rate.
    """
    
    scope = "burst_user"
    rate = "600/minute"


class SensitiveAnonRateThrottle(AnonRateThrottle):
    """
    Throttle for anonymous users accessing sensitive endpoints.
    """
    
    scope = "sensitive_anon"
    rate = "3/minute"


class SensitiveUserRateThrottle(UserRateThrottle):
    """
    Throttle for authenticated users accessing sensitive endpoints.
    """
    
    scope = "sensitive_user"
    rate = "10/minute"
