from rest_framework import serializers
from .models import *
from datetime import datetime

SEVERITY_ORDERS = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "info": 1,
    "": 0,
}


def calculate_severity(base_score):
    if base_score is None:
        return None
    try:
        base_score = float(base_score)

        if base_score == 0:
            return "info"
        elif base_score > 0 and base_score <= 3.9:
            return "low"
        elif base_score >= 4.0 and base_score <= 6.9:
            return "medium"
        elif base_score >= 7.0 and base_score <= 8.9:
            return "high"
        elif base_score >= 9.0 and base_score <= 10.0:
            return "critical"
        else:
            return f""

    except:
        return f""


class ScannerMasterVulnerabilityTemplateSerializer(serializers.ModelSerializer):
    cve = serializers.SerializerMethodField(source="cve")
    cwe = serializers.SerializerMethodField(source="cwe")

    class Meta:
        model = ScannerMasterVulnerabilityTemplate
        fields = "__all__"

    def get_cve(self, instance):
        if isinstance(instance.cve, list):
            return ", ".join(instance.cve)
        return instance.cve

    def get_cwe(self, instance):
        if isinstance(instance.cwe, list):
            return ", ".join(instance.cwe)
        return instance.cwe


class ScannerMasterVulnerabilityTemplatePreviewSerializer(serializers.ModelSerializer):
    severity = serializers.SerializerMethodField(read_only=True)
    severity_order = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ScannerMasterVulnerabilityTemplate
        fields = ["id", "name", "cvss_version", "cvss_vector", "cvss_base_score", "severity", "severity_order"]

    def get_severity(self, instance):
        return calculate_severity(instance.cvss_base_score)

    def get_severity_order(self, instance):
        return SEVERITY_ORDERS[calculate_severity(instance.cvss_base_score)]


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
