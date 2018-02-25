from rest_framework import permissions
from django.http import HttpResponse

class IsOwnerOrReadOnly(permissions.BasePermission):
	'''
	Custom permission to only owners of an object to edit it
	'''
	def has_object_permission(self, request, view, obj):
		# read permissions are allowed t any request,
		# so we'll always allow GET, HEAD or OPTIONS reqeusts
		print "request.method:{}, permissions.method:{}, obj:{}".format(request.method, permissions.SAFE_METHODS, obj)
		if request.method in permissions.SAFE_METHODS:
			return True
		# write permissions are only allowed to the owner of the snippet
		return obj.owner == request.user			