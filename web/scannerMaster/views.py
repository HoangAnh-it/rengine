from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from dashboard.models import Project
from django.db.models import F
from .serializers import ScannerMasterVulnerabilityTemplatePreviewSerializer


def list_targets(request, slug):
    project = Project.objects.get(slug=slug)
    targets = ScannerMasterTarget.objects.all().order_by("-created_at")
    context = {
        "scanner_master_nav_active": True,
        "targets": DetailTargetSerializer(instance=targets, many=True).data,
        "current_project": project,
    }
    return render(request, "list.html", context)


def detail_target(request, slug, id):
    target = ScannerMasterTarget.objects.filter(id=id)
    vul_template_id = request.GET.get("vul_template")
    template = "list-vuls.html" if not vul_template_id else "detail.html"

    if not target.exists():
        target = None
    else:
        target = target.get()

    results = ScannerMasterResult.objects.filter(target_id=id)
    vulnerability_template_ids = set(results.values_list("vulnerability_template_id", flat=True))
    vulnerabilities = ScannerMasterVulnerabilityTemplatePreviewSerializer(instance=ScannerMasterVulnerabilityTemplate.objects.filter(id__in=vulnerability_template_ids), many=True).data
    vulnerabilities.sort(key=lambda v: (-v["severity_order"], -float(v["cvss_base_score"])))

    list_urls = ScannerMasterResult.objects.filter(vulnerability_template=vul_template_id).distinct("url")
    vul_template = ScannerMasterVulnerabilityTemplate.objects.get(id=vul_template_id) if vul_template_id else None

    context = {
        "target": DetailTargetSerializer(instance=target).data,
        "vulnerabilities": vulnerabilities,
        "list_urls": ScannerMasterResultSerializer(instance=list_urls, many=True).data,
        "vul_template_active": vul_template_id,
        "vulnerability_template": ScannerMasterVulnerabilityTemplateSerializer(instance=vul_template).data if vul_template_id else None,
    }

    return render(request, template, context)
