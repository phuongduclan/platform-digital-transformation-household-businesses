"""
Datetime utilities for Vietnam timezone (GMT+7)
"""
from datetime import datetime, timezone, timedelta

# Vietnam timezone: UTC+7
VIETNAM_TZ = timezone(timedelta(hours=7))

def vietnam_now():
    """
    Get current datetime in Vietnam timezone (GMT+7)
    Returns datetime without timezone info (naive) for SQL Server compatibility
    """
    return datetime.now(VIETNAM_TZ).replace(tzinfo=None)

def utc_to_vietnam(utc_dt):
    """
    Convert UTC datetime to Vietnam timezone
    """
    if utc_dt is None:
        return None
    if utc_dt.tzinfo is None:
        # Assume UTC if no timezone
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(VIETNAM_TZ).replace(tzinfo=None)

def vietnam_to_utc(vietnam_dt):
    """
    Convert Vietnam datetime to UTC
    """
    if vietnam_dt is None:
        return None
    if vietnam_dt.tzinfo is None:
        # Assume Vietnam timezone
        vietnam_dt = vietnam_dt.replace(tzinfo=VIETNAM_TZ)
    return vietnam_dt.astimezone(timezone.utc).replace(tzinfo=None)
