# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa

# Users
from app.models.user.user_types import User_Types  # noqa
from app.models.user.user_roles import User_Roles  # noqa
from app.models.user.user_info import User_Info  # noqa
from app.models.user.user_action_audit import User_Audit_Trail  # noqa

# Documents
from app.models.documents.document_class import Document_Class # noqa
from app.models.documents.document_category import Document_Category # noqa
from app.models.documents.document_user import Document_User # noqa
from app.models.documents.document_action_audit import Document_Audit_Trail # noqa


