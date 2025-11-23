from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'description', 'category', 'date']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Automatically assign the transaction to the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)