"""
Views contain the actual logic for handling API requests.
Each view corresponds to one or more of our API endpoints.

We use DRF's APIView class to keep things explicit and beginner-friendly.
"""

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer


class StudentListCreateView(APIView):

    def get(self, request):
        search_query = request.query_params.get('search', '').strip()

        students = Student.objects.all()

        if search_query:
            students = students.filter(
                Q(name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(department__icontains=search_query)
            )

        serializer = StudentSerializer(students, many=True)

        return Response(
            {
                "success": True,
                "count": students.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Student created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "message": "Failed to create student. Please check the errors below.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentDetailView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)

        return self._update(serializer)

    def patch(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        return self._update(serializer)

    def _update(self, serializer):
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Student updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "message": "Failed to update student. Please check the errors below.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        student = self.get_object(pk)
        student_name = student.name
        student.delete()

        return Response(
            {
                "success": True,
                "message": f"Student '{student_name}' deleted successfully."
            },
            status=status.HTTP_200_OK
        )
