from rest_framework import serializers
from .models import *
from datetime import datetime


class ScannerMasterVulnerabilityTemplateSerializer(serializers.ModelSerializer):
    cve = serializers.SerializerMethodField(source="cve")
    cwe = serializers.SerializerMethodField(source="cwe")

    class Meta:
        model = ScannerMasterVulnerabilityTemplate
        fields = "__all__"

    def get_cve(self, instance):
        return ", ".join(instance.cve)

    def get_cwe(self, instance):
        return ", ".join(instance.cwe)


class DetailTargetSerializer(serializers.ModelSerializer):
    vulnerability_template = ScannerMasterVulnerabilityTemplateSerializer(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ScannerMasterTarget
        fields = "__all__"

    def get_created_at(self, target):
        return datetime.utcfromtimestamp(target.created_at).strftime("%Y-%m-%d %H:%M:%S")


class CreateScannerMasterResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannerMasterResult
        fields = "__all__"


class ScannerMasterResultSerializer(serializers.ModelSerializer):
    vulnerability_template = ScannerMasterVulnerabilityTemplateSerializer(read_only=True)

    class Meta:
        model = ScannerMasterResult
        fields = "__all__"
