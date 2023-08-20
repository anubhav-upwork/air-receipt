"""
    SUPERADMIN = 2
    USER = 1
    TENANT = 0
    REVIEWER = -1
"""

USER_ROLES_DATA = [
    {
        "user_role": "superadmin",
        "user_access_level": 2
        # Full access - create, delete edit or change user details of everyone and documents
    },
    {
        "user_role": "user",
        "user_access_level": 1
        # Restricted access - create, edit or change user details
    },
    {
        "user_role": "tenant",
        "user_access_level": 0
        # Little access, can upload - Temporary user for trial purpose, once trial done promoted to user, can be used
        # for marketing
    },
    {
        "user_role": "reviewer",
        "user_access_level": -1
        # No access apart from reviewing documents
    }
]
