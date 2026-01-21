from flask import Blueprint, jsonify
from infrastructure.databases.mssql import session
from sqlalchemy import text, func
from api.decorators.auth_decorators import require_permission
from infrastructure.databases.session_utils import safe_rollback
from datetime import datetime

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/api/admin/dashboard')

@admin_dashboard_bp.route('/stats', methods=['GET'])
@require_permission(function_code="F004", methods=["GET"])
def get_dashboard_stats():
    """
    Get dashboard statistics (Admin only)
    ---
    get:
      summary: Get dashboard statistics
      security:
        - Bearer: []
      tags:
        - Admin Dashboard
      responses:
        200:
          description: Dashboard statistics
          content:
            application/json:
              schema:
                type: object
                properties:
                  total_owners:
                    type: integer
                    example: 42
                  subscriptions_active:
                    type: integer
                    example: 38
                  subscription_plans:
                    type: integer
                    example: 5
                  revenue_this_month:
                    type: number
                    example: 8500000
    """
    try:
        # Total Owners (role_id = 2)
        total_owners_query = text("""
            SELECT COUNT(*) as count
            FROM users
            WHERE role_id = 2 AND status = 'Active'
        """)
        total_owners_result = session.execute(total_owners_query).fetchone()
        total_owners = total_owners_result[0] if total_owners_result else 0

        # Active Subscriptions
        subscriptions_active_query = text("""
            SELECT COUNT(*) as count
            FROM subscriptions
            WHERE is_active = true
        """)
        subscriptions_active_result = session.execute(subscriptions_active_query).fetchone()
        subscriptions_active = subscriptions_active_result[0] if subscriptions_active_result else 0

        # Total Subscription Plans
        subscription_plans_query = text("""
            SELECT COUNT(*) as count
            FROM subscriptionplans
        """)
        subscription_plans_result = session.execute(subscription_plans_query).fetchone()
        subscription_plans = subscription_plans_result[0] if subscription_plans_result else 0

        # Revenue this month (sum of subscription plan prices for active subscriptions this month)
        # Note: This is a simplified calculation. In production, you might want to track actual payments.
        revenue_query = text("""
            SELECT COALESCE(SUM(sp.price), 0) as revenue
            FROM subscriptions s
            INNER JOIN subscriptionplans sp ON s.plan_id = sp.id
            WHERE s.is_active = true
            AND EXTRACT(MONTH FROM s.start_date) = EXTRACT(MONTH FROM NOW())
            AND EXTRACT(YEAR FROM s.start_date) = EXTRACT(YEAR FROM NOW())
        """)
        revenue_result = session.execute(revenue_query).fetchone()
        revenue_this_month = float(revenue_result[0]) if revenue_result and revenue_result[0] else 0.0

        return jsonify({
            'total_owners': total_owners,
            'subscriptions_active': subscriptions_active,
            'subscription_plans': subscription_plans,
            'revenue_this_month': revenue_this_month
        }), 200
    except Exception as e:
        safe_rollback(session)
        return jsonify({'error': str(e)}), 500

@admin_dashboard_bp.route('/analytics', methods=['GET'])
@require_permission(function_code="F004", methods=["GET"])
def get_analytics():
    """
    Get analytics data (Admin only)
    ---
    get:
      summary: Get analytics data
      security:
        - Bearer: []
      tags:
        - Admin Dashboard
      responses:
        200:
          description: Analytics data
    """
    try:
        # Total Users (all roles)
        total_users_query = text("""
            SELECT COUNT(*) as count
            FROM users
            WHERE status = 'Active'
        """)
        total_users_result = session.execute(total_users_query).fetchone()
        total_users = total_users_result[0] if total_users_result else 0

        # New Subscriptions this month
        new_subscriptions_query = text("""
            SELECT COUNT(*) as count
            FROM subscriptions
            WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW())
            AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())
        """)
        new_subscriptions_result = session.execute(new_subscriptions_query).fetchone()
        new_subscriptions = new_subscriptions_result[0] if new_subscriptions_result else 0

        # Active Households
        active_households_query = text("""
            SELECT COUNT(DISTINCT h.id) as count
            FROM households h
            INNER JOIN subscriptions s ON h.id = s.household_id
            WHERE s.is_active = true
        """)
        active_households_result = session.execute(active_households_query).fetchone()
        active_households = active_households_result[0] if active_households_result else 0

        # User growth (last 7 days)
        user_growth_query = text("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM users
            WHERE created_at >= NOW() - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        user_growth_results = session.execute(user_growth_query).fetchall()
        user_growth = [0] * 7
        today = datetime.now().date()
        for row in user_growth_results:
            date = row[0]
            count = row[1]
            days_ago = (today - date).days
            if 0 <= days_ago < 7:
                user_growth[6 - days_ago] = count

        # Monthly subscriptions (last 6 months)
        monthly_subscriptions_query = text("""
            SELECT EXTRACT(MONTH FROM created_at) as month, 
                   EXTRACT(YEAR FROM created_at) as year, 
                   COUNT(*) as count
            FROM subscriptions
            WHERE created_at >= NOW() - INTERVAL '6 months'
            GROUP BY EXTRACT(MONTH FROM created_at), EXTRACT(YEAR FROM created_at)
            ORDER BY year, month
        """)
        monthly_subscriptions_results = session.execute(monthly_subscriptions_query).fetchall()
        monthly_subscriptions = [0] * 6
        for i, row in enumerate(monthly_subscriptions_results):
            if i < 6:
                monthly_subscriptions[i] = row[2]

        # Household activity (active/inactive by month, last 6 months)
        household_activity_query = text("""
            SELECT 
                EXTRACT(MONTH FROM s.created_at) as month,
                EXTRACT(YEAR FROM s.created_at) as year,
                SUM(CASE WHEN s.is_active = true THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN s.is_active = false THEN 1 ELSE 0 END) as inactive
            FROM subscriptions s
            WHERE s.created_at >= NOW() - INTERVAL '6 months'
            GROUP BY EXTRACT(MONTH FROM s.created_at), EXTRACT(YEAR FROM s.created_at)
            ORDER BY year, month
        """)
        household_activity_results = session.execute(household_activity_query).fetchall()
        household_activity = {
            'active': [0] * 6,
            'inactive': [0] * 6
        }
        for i, row in enumerate(household_activity_results):
            if i < 6:
                household_activity['active'][i] = row[2] or 0
                household_activity['inactive'][i] = row[3] or 0

        return jsonify({
            'total_users': total_users,
            'new_subscriptions': new_subscriptions,
            'active_households': active_households,
            'user_growth': user_growth,
            'monthly_subscriptions': monthly_subscriptions,
            'household_activity': household_activity
        }), 200
    except Exception as e:
        safe_rollback(session)
        return jsonify({'error': str(e)}), 500
