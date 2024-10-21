from rest_framework import serializers
from .models import *
from datetime import datetime


class TargetSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ScannerMasterTarget
        fields = "__all__"

    def get_created_at(self, target):
        return datetime.utcfromtimestamp(target.created_at).strftime("%Y-%m-%d %H:%M:%S")


class ScannerMasterVulnerabilityTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannerMasterVulnerabilityTemplate
        fields = "__all__"


class DetailTargetSerializer(serializers.ModelSerializer):
    vulnerability_template = ScannerMasterVulnerabilityTemplateSerializer(read_only=True)

    class Meta:
        model = ScannerMasterTarget
        fields = "__all__"


class ScannerMasterResultSerializer(serializers.ModelSerializer):
    vulnerability_template = ScannerMasterVulnerabilityTemplateSerializer(read_only=True)

    class Meta:
        model = ScannerMasterResult
        fields = "__all__"
