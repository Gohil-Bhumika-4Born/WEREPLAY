"""
All issues page routes.
"""
from flask import render_template
from flask_login import login_required
from . import main_bp

@main_bp.route('/all-issues')
@login_required
def all_issues():
    """
    Render the all issues page.
    """
    from flask import request
    
    # Mock Issue Data
    mock_issues = [
        {
            'id': 1,
            'title': 'Payment issue',
            'description': 'Customers reporting payment processing failures, transaction errors, and refund delays.',
            'priority': 'High Priority',
            'priority_color': 'red',
            'affected': '150+',
            'updated': '2 hours ago',
            'icon_color': 'red',
            'icon_bg': 'red-500' # used for the dot
        },
        {
            'id': 2,
            'title': 'Account access',
            'description': 'Users unable to access their accounts, login problems, and password reset issues.',
            'priority': 'Medium Priority',
            'priority_color': 'orange',
            'affected': '85+',
            'updated': '5 hours ago',
            'icon_color': 'orange',
            'icon_bg': 'orange-500'
        },
        {
            'id': 3,
            'title': 'Product inquiry',
            'description': 'Questions about product features, pricing, availability, and specifications.',
            'priority': 'Normal Priority',
            'priority_color': 'yellow',
            'affected': '62+',
            'updated': '1 day ago',
            'icon_color': 'yellow',
            'icon_bg': 'yellow-500'
        },
        {
            'id': 4,
            'title': 'Technical support',
            'description': 'Requests for help with app glitches, installation problems, and feature usage.',
            'priority': 'Normal Priority',
            'priority_color': 'blue',
            'affected': '45+',
            'updated': '2 days ago',
            'icon_color': 'blue',
            'icon_bg': 'blue-500'
        },
        {
            'id': 5,
            'title': 'Refund request',
            'description': 'Formal requests for refunds based on return policies or service dissatisfaction.',
            'priority': 'Low Priority',
            'priority_color': 'purple',
            'affected': '28+',
            'updated': '3 days ago',
            'icon_color': 'purple',
            'icon_bg': 'purple-500'
        },
         # Duplicate some data for pagination demo
        {
            'id': 6,
            'title': 'Login Failure',
            'description': 'Users reporting intermittent 500 errors during login.',
            'priority': 'High Priority',
            'priority_color': 'red',
            'affected': '40+',
            'updated': '4 hours ago',
            'icon_color': 'red',
            'icon_bg': 'red-500'
        },
        {
            'id': 7,
            'title': 'Invoice Generation',
            'description': 'Invoices are not being generated for new subscriptions.',
            'priority': 'Medium Priority',
            'priority_color': 'orange',
            'affected': '12+',
            'updated': '6 hours ago',
            'icon_color': 'orange',
            'icon_bg': 'orange-500'
        },
         {
            'id': 8,
            'title': 'Mobile App Crash',
            'description': 'App crashes when opening the settings menu on iOS.',
            'priority': 'High Priority',
            'priority_color': 'red',
            'affected': '200+',
            'updated': '1 hour ago',
            'icon_color': 'red',
            'icon_bg': 'red-500'
        },
         {
            'id': 9,
            'title': 'Email Delivery',
            'description': 'Reset password emails are delayed by 10 minutes.',
            'priority': 'Low Priority',
            'priority_color': 'blue',
            'affected': '15+',
            'updated': '1 day ago',
            'icon_color': 'blue',
            'icon_bg': 'blue-500'
        },
         {
            'id': 10,
            'title': 'Feature Request',
            'description': 'Users asking for dark mode in the mobile app.',
            'priority': 'Low Priority',
            'priority_color': 'purple',
            'affected': '50+',
            'updated': '2 days ago',
            'icon_color': 'purple',
            'icon_bg': 'purple-500'
        },
         {
            'id': 11,
            'title': 'API Rate Limit',
            'description': 'Users hitting API rate limits unexpectedly.',
            'priority': 'Medium Priority',
            'priority_color': 'orange',
            'affected': '30+',
            'updated': '5 hours ago',
            'icon_color': 'orange',
            'icon_bg': 'orange-500'
        },
         {
            'id': 12,
            'title': 'Data Export',
            'description': 'CSV export fails for large datasets.',
            'priority': 'Normal Priority',
            'priority_color': 'yellow',
            'affected': '10+',
            'updated': '3 days ago',
            'icon_color': 'yellow',
            'icon_bg': 'yellow-500'
        }
    ]

    # Pagination Logic
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int) # default 5 to show pagination with 12 items
    
    total = len(mock_issues)
    start = (page - 1) * per_page
    end = start + per_page
    items = mock_issues[start:end]
    
    class MockPagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            
        @property
        def has_prev(self):
            return self.page > 1
            
        @property
        def has_next(self):
            return self.page < self.pages
            
        @property
        def prev_num(self):
            return self.page - 1
            
        @property
        def next_num(self):
            return self.page + 1
            
        def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
            last = 0
            for num in range(1, self.pages + 1):
                if num <= left_edge or \
                   (num > self.page - left_current - 1 and \
                    num < self.page + right_current) or \
                   num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    pagination = MockPagination(items, page, per_page, total)

    return render_template('main/all-issues.html', pagination=pagination)
