# Generated by Django 3.2.23 on 2024-10-21 07:43

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import time


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ScannerMasterTarget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.FloatField(auto_created=True, default=time.time)),
                ("website", models.URLField()),
                ("status", models.CharField(choices=[("Scanning", "Scanning"), ("Done", "Done"), ("Error", "Error")], default="Scanning", max_length=100)),
            ],
            options={
                "db_table": "scannerMaster_target",
            },
        ),
        migrations.CreateModel(
            name="ScannerMasterVulnerabilityTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("cve", django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), blank=True, default=list, size=None)),
                ("cwe", django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), blank=True, default=list, size=None)),
                ("impact", models.TextField(blank=True, null=True)),
                ("affected", models.TextField(blank=True, null=True)),
                ("solution", models.TextField(blank=True, null=True)),
                ("references_links", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=list, null=True), size=None)),
                ("cvss_version", models.CharField(max_length=255)),
                ("cvss_vector", models.CharField(max_length=255)),
                ("cvss_base_score", models.DecimalField(decimal_places=1, default=None, max_digits=5, null=True)),
                ("file_name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "scannerMaster_vulnerability_template",
            },
        ),
        migrations.CreateModel(
            name="ScannerMasterResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("url", models.URLField()),
                ("target_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="target", to="scannerMaster.scannermastertarget")),
                (
                    "vulnerability_template",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vulnerability_template", to="scannerMaster.scannermastervulnerabilitytemplate"),
                ),
                ("attack_detail", models.TextField(blank=True, null=True)),
                ("attack_detail_en", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "scannerMaster_result",
            },
        ),
    ]