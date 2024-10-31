from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from dashboard.models import Project


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
    detail_id = request.GET.get("link_id")
    detail = ScannerMasterResult.objects.get(id=detail_id) if detail_id else None

    if not target.exists():
        target = None
    else:
        target = target.get()

    results = ScannerMasterResult.objects.filter(target_id=id)
    links = []
    for r in results.distinct("url"):
        links.append(
            {
                "link": r.url,
                "id": r.id,
                "is_active": r.id == detail_id,
                "target_id": target.id,
            }
        )

    context = {
        "target": DetailTargetSerializer(instance=target).data,
        "links": links,
        "vulnerabilities": ScannerMasterResultSerializer(instance=ScannerMasterResult.objects.filter(url=detail.url).distinct("vulnerability_template"), many=True).data if detail else [],
    }

    return render(request, "detail.html", context)
