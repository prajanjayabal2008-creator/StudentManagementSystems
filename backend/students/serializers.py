"""
Serializers convert Student model instances to JSON (for API responses)
and validate incoming JSON data (for creating/updating students).

This is where most of our SERVER-SIDE validation lives.
"""

from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'name',
            'email',
            'department',
            'year',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_student_id(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Student ID cannot be empty.")

        queryset = Student.objects.filter(student_id__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A student with this Student ID already exists."
            )

        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long."
            )
        return value

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = Student.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A student with this email already exists."
            )

        return value

    def validate_department(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Department cannot be empty.")
        return value

    def validate_year(self, value):
        if value not in [1, 2, 3, 4]:
            raise serializers.ValidationError(
                "Year must be 1, 2, 3, or 4."
            )
        return value
