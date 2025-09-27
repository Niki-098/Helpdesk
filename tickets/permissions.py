from rest_framework import permissions

class IsTicketOwnerOrAdminOrAgent(permissions.BasePermission):
    """
    - Users can access only their own tickets
    - Agents can access tickets assigned to them
    - Admins can access everything
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'ADMIN':
            return True
        if user.role == 'AGENT' and obj.assigned_to and obj.assigned_to.id == user.id:
            return True
        # default: owner
        return obj.created_by.id == user.id
