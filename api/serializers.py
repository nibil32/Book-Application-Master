from rest_framework import serializers

from book.models import Books


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:

        model=Books
        fields="__all__"