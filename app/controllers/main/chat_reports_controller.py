"""
Chat Reports controller for handling chat reports-related requests.
"""
from flask import render_template, request, redirect, url_for
from flask_login import login_required


class ChatReportsController:
    """Controller for chat reports pages."""
    
    @staticmethod
    @login_required
    def chat_reports_page():
        """Render chat reports page with data from database."""
        from app.models.chat_report import ChatReport
        from flask_login import current_user
        from sqlalchemy import or_
        from datetime import datetime
        from app.extensions import db
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        sentiment = request.args.get('sentiment', '').strip()
        category = request.args.get('category', '').strip()
        date_from = request.args.get('date_from', '').strip()
        date_to = request.args.get('date_to', '').strip()
        min_messages = request.args.get('min_messages', type=int)
        max_messages = request.args.get('max_messages', type=int)

        # Base Query
        query = ChatReport.query.filter_by(app_id=str(current_user.id))

        # Search Filter
        if search:
            search_terms = search.split()
            for term in search_terms:
                term_like = f"%{term}%"
                query = query.filter(
                    or_(
                        ChatReport.title.ilike(term_like),
                        ChatReport.description.ilike(term_like)
                    )
                )

        # Apply Filters
        if sentiment:
            query = query.filter(ChatReport.sentiment == sentiment.upper())
        if category:
            query = query.filter(ChatReport.category == category)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(ChatReport.updated_at >= date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                # Add one day to include the end date fully
                query = query.filter(ChatReport.updated_at <= date_to_obj.replace(hour=23, minute=59, second=59))
            except ValueError:
                pass
            
        if min_messages is not None:
            query = query.filter(ChatReport.message_count >= min_messages)
        if max_messages is not None:
            query = query.filter(ChatReport.message_count <= max_messages)

        # Pagination
        pagination = query.order_by(ChatReport.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Calculate Global Stats (across all user's reports, not just filtered view)
        from sqlalchemy import func
        stats_query = ChatReport.query.filter_by(app_id=str(current_user.id))
        
        total_reports = stats_query.count()
        frustrated_count = stats_query.filter(ChatReport.sentiment == 'FRUSTRATED').count()
        positive_count = stats_query.filter(ChatReport.sentiment == 'POSITIVE').count()
        
        avg_msg_result = db.session.query(func.avg(ChatReport.message_count))\
            .filter(ChatReport.app_id == str(current_user.id)).scalar() or 0
        
        stats = {
            'total': total_reports,
            'frustrated': frustrated_count,
            'positive_percent': round((positive_count / total_reports * 100)) if total_reports > 0 else 0,
            'avg_messages': round(avg_msg_result)
        }
        
        return render_template(
            'main/chat-reports.html', 
            pagination=pagination,
            stats=stats,
            filters={
                'search': search,
                'sentiment': sentiment,
                'category': category,
                'date_from': date_from,
                'date_to': date_to,
                'min_messages': min_messages,
                'max_messages': max_messages,
                'page': page,
                'per_page': per_page
            }
        )
    
    @staticmethod
    @login_required
    def chat_reports_details_page():
        """Render chat reports details page."""
        topic_id = request.args.get('topicId')
        if not topic_id:
            return redirect(url_for('main.chat_reports'))
            
        from app.models.chat_report import ChatReport
        from flask_login import current_user
        
        # Verify the report belongs to the current user
        # User confirmed app_id matches user.id (integer)
        report = ChatReport.query.filter_by(id=topic_id, app_id=str(current_user.id)).first_or_404()
        
        return render_template('main/chat-reports-details.html', report=report)
