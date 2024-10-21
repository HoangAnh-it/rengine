from django.apps import apps
from django.db import models
import time
from django.contrib.postgres.fields import ArrayField


class ScannerMasterTarget(models.Model):
    class Meta:
        db_table = "scannerMaster_target"

    website = models.URLField(blank=False, null=False)
    status = models.CharField(
        max_length=100,
        choices=[
            ("Scanning", "Scanning"),
            ("Done", "Done"),
            ("Error", "Error"),
        ],
        default="Scanning",
    )
    created_at = models.FloatField(default=time.time, auto_created=True)


class ScannerMasterVulnerabilityTemplate(models.Model):
    class Meta:
        db_table = "scannerMaster_vulnerability_template"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    cve = ArrayField(models.CharField(max_length=255, null=True, blank=False), default=list, blank=True)
    cwe = ArrayField(models.CharField(max_length=255, null=True, blank=False), default=list, blank=True)
    impact = models.TextField(null=True, blank=True)
    affected = models.TextField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    references_links = ArrayField(models.TextField(blank=True, null=True, default=list))
    cvss_version = models.CharField(max_length=255, null=False, blank=False)
    cvss_vector = models.CharField(max_length=255, null=False, blank=False)
    cvss_base_score = models.DecimalField(max_digits=5, decimal_places=1, blank=False, null=True, default=None)
    file_name = models.CharField(max_length=255, null=False, blank=False)


class ScannerMasterResult(models.Model):
    class Meta:
        db_table = "scannerMaster_result"

    target_id = models.ForeignKey(ScannerMasterTarget, on_delete=models.CASCADE, null=False, related_name="target")
    vulnerability_template = models.ForeignKey(ScannerMasterVulnerabilityTemplate, on_delete=models.CASCADE, null=False, related_name="vulnerability_template")

    url = models.URLField(blank=False, null=False)
    attack_detail = models.TextField(null=True, blank=True)
    attack_detail_en = models.TextField(null=True, blank=True)
