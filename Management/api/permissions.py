from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

class IsLibrarian(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'

class IsUser(BasePermission):

    def  has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None ) == 'user'
    





# class IsAdminOrReadOnly(permissions.IsAdminUser):

#     def has_permission(self, request):
#             if request.method in permissions.SAFE_METHODS:
#                 return True
#             else:
#                 return bool(request.user and request.user.is_staff)
        

# class IsReviewUserOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         else:
#             return obj.review_user == request.user or request.user.is_staff