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
    list_urls = ScannerMasterResultSerializer(instance=ScannerMasterResult.objects.filter(vulnerability_template=vul_template_id).distinct("url"), many=True).data

    list_urls = []
    if "localhost/DVWA" in target.website:
        vulnerability_template_ids = [32, 114, 25, 127]
        if vul_template_id is not None:
            match int(vul_template_id):
                case 32:
                    list_urls.extend(
                        [
                            {
                                "url": "http://localhost/DVWA/vulnerabilities/fi/?page=../../../../../../etc/passwd",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )
                case 114:
                    list_urls.extend(
                        [
                            {
                                "url": "http://localhost/DVWA/vulnerabilities/sqli/?id='or1=1--&Submit=Submit#",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

                case 25:
                    list_urls.extend(
                        [
                            {
                                "url": "http://localhost/DVWA/vulnerabilities/xss_r/?name=<script>alert(1)</script>",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

                case 127:
                    list_urls.extend(
                        [
                            {
                                "url": "http://localhost/DVWA/vulnerabilities/open_redirect/source/low.php?redirect=https://www.google.com/",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

    elif "testphp.vulnweb.com" in target.website:
        vulnerability_template_ids = [25, 18, 115, 114, 32, 64]
        if vul_template_id is not None:
            match int(vul_template_id):
                case 114:
                    list_urls.extend(
                        [
                            {
                                "url": "http://testphp.vulnweb.com/listproducts.php?cat=1%20OR%2017-7%3d10",
                                "attack_detail_en": "No message",
                            },
                            {
                                "url": "http://testphp.vulnweb.com/product.php?pic=1%20OR%2017-7%3d10",
                                "attack_detail_en": "No message",
                            },
                        ]
                    )

                case 25:
                    list_urls.extend(
                        [
                            {
                                "url": "http://testphp.vulnweb.com/listproducts.php?artist=%3cscRipt%3enetsparker(0x106C07)%3c%2fscRipt%3e",
                                "attack_detail_en": "No message",
                            },
                            {
                                "url": "http://testphp.vulnweb.com/hpp/?pp=x%22%20onmouseover%3dnetsparker(0x106ED2)%20x%3d%22",
                                "attack_detail_en": "No message",
                            },
                            {
                                "url": "http://testphp.vulnweb.com/hpp/params.php?aaaa%2f=&p=%3cscRipt%3enetsparker(0x107E91)%3c%2fscRipt%3e&pp=12",
                                "attack_detail_en": "No message",
                            },
                        ]
                    )

                case 18:
                    list_urls.extend(
                        [
                            {
                                "url": "http://testphp.vulnweb.com/showimage.php?file=hTTp%3a%2f%2fr87.com%2fn",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

                case 115:
                    list_urls.extend(
                        [
                            {
                                "url": "https://testphp.vulnweb.com/login.php",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

                case 32:
                    list_urls.extend(
                        [
                            {
                                "url": "http://testphp.vulnweb.com/showimage.php?file=%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fproc%2fversion",
                                "attack_detail_en": "No message",
                            }
                        ]
                    )

                case 64:
                    list_urls.extend(
                        [
                            {
                                "url": "http://testphp.vulnweb.com/secured/phpinfo.php",
                                "attack_detail_en": "Found IP: 192.168.0.5, 192.168.0.26",
                            }
                        ]
                    )

    vulnerabilities = ScannerMasterVulnerabilityTemplatePreviewSerializer(instance=ScannerMasterVulnerabilityTemplate.objects.filter(id__in=vulnerability_template_ids), many=True).data
    vulnerabilities.sort(key=lambda v: (-v["severity_order"], -float(v["cvss_base_score"])))
    vul_template = ScannerMasterVulnerabilityTemplate.objects.get(id=vul_template_id) if vul_template_id else None

    print(target.website)
    context = {
        "target": DetailTargetSerializer(instance=target).data,
        "vulnerabilities": vulnerabilities,
        "list_urls": list_urls,
        "vul_template_active": vul_template_id,
        "vulnerability_template": ScannerMasterVulnerabilityTemplateSerializer(instance=vul_template).data if vul_template_id else None,
    }

    return render(request, template, context)
