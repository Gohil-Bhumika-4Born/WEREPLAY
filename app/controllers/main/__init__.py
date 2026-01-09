"""
Main application controllers package.
"""
from .dashboard_controller import DashboardController
from .profile_controller import ProfileController
from .documents_controller import DocumentsController
from .ai_training_controller import AITrainingController
from .chat_reports_controller import ChatReportsController
from .guidelines_controller import GuidelinesController
from .notifications_controller import NotificationsController
from .plans_billing_controller import PlansBillingController
from .download_software_controller import DownloadSoftwareController
from .support_controller import SupportController
from .terms_conditions_controller import TermsConditionsController
from .api_controller import ApiController

__all__ = [
    'DashboardController',
    'ProfileController',
    'DocumentsController',
    'AITrainingController',
    'ChatReportsController',
    'GuidelinesController',
    'NotificationsController',
    'PlansBillingController',
    'DownloadSoftwareController',
    'SupportController',
    'TermsConditionsController',
    'ApiController',
]
