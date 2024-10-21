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
        "targets": TargetSerializer(instance=targets, many=True).data,
        "current_project": project,
    }
    context = {
        "targets": [
            {
                "id": 1,
                "website": "https://bwapp.hakhub.ne",
                "status": "Scanning",
                "created_at": "	2024-10-21 16:41:19",
            },
            {
                "id": 2,
                "website": "http://testphp.vulnweb.com/",
                "status": "Done",
                "created_at": "	2024-10-21 16:41:19",
            },
            {
                "id": 3,
                "website": "https://pms.dev.cyradar.com",
                "status": "Error",
                "created_at": "2024-10-21 16:40:46",
            },
            {
                "id": 4,
                "website": "https://baoviet.com.vn/vi",
                "status": "Done",
                "created_at": "2024-10-21 17:01:44",
            },
        ]
    }
    return render(request, "list.html", context)


def detail_target(request, slug, id):
    # target = ScannerMasterTarget.objects.filter(id=id)

    # if not target.exists():
    #     target = None
    # else:
    #     target = target.get()

    # context = {
    #     target: DetailTargetSerializer(instance=target).data,
    # }
    data = {
        "1": {"url": "https://bwapp.hakhub.net/sqli_2.php?movie=%27or1=1--&action=go"},
        "2": {"url": "https://bwapp.hakhub.net/xss_get.php?firstname=%3Cscript%3Ealert%281%29%3C%2Fscript%3E&lastname=%3Cscript%3Ealert%281%29%3C%2Fscript%3E&form=submit"},
        "3": {
            "url": "https://bwapp.hakhub.net/directory_traversal_1.php?page=/etc/passwd",
        },
        "4": {
            "url": "https://bwapp.hakhub.net/backdoor.php",
        },
    }

    data_vul = {
        "1": [
            {
                "name": "SQL Injection Vulnerability",
                "description": "SQL Injection may allow attackers to execute arbitrary SQL commands.",
                "cve": ["CVE-2021-11111"],
                "cwe": ["CWE-89"],
                "impact": "Database integrity may be compromised.",
                "affected": "Web applications that fail to properly sanitize inputs.",
                "solution": "Implement prepared statements and input validation.",
                "references_links": ["https://nvd.nist.gov/vuln/detail/CVE-2021-11111"],
                "cvss_version": "3.1",
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "cvss_base_score": 9.0,
            }
        ],
        "2": [
            {
                "name": "Cross-Site Scripting (XSS)",
                "description": "A vulnerability where attackers inject malicious scripts into web pages.",
                "cve": ["CVE-2020-4567"],
                "cwe": ["CWE-79"],
                "impact": "Attackers may steal session tokens or impersonate users.",
                "affected": "Web applications with improper input sanitization.",
                "solution": "Sanitize inputs and apply proper output encoding.",
                "references_links": ["https://nvd.nist.gov/vuln/detail/CVE-2020-4567"],
                "cvss_version": "3.1",
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
                "cvss_base_score": 6.1,
            }
        ],
        "3": [
            {
                "name": "Directory Traversal Vulnerability",
                "description": "A directory traversal vulnerability allows attackers to access files outside the intended directory.",
                "cve": ["CVE-2020-12345"],
                "cwe": ["CWE-22"],
                "impact": "Sensitive files may be accessed by traversing directories.",
                "affected": "Web applications with inadequate input validation.",
                "solution": "Sanitize user inputs and restrict file access.",
                "references_links": ["https://nvd.nist.gov/vuln/detail/CVE-2020-12345"],
                "cvss_version": "3.1",
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                "cvss_base_score": 8.8,
            }
        ],
        "4": [
            {
                "name": "Backup File Disclosure",
                "description": "A backup file is publicly accessible, which may expose sensitive information.",
                "cve": ["CVE-2021-23333"],
                "cwe": ["CWE-200"],
                "impact": "An attacker can download the backup file and access sensitive information.",
                "affected": "N/A",
                "solution": "Remove or secure backup files from public access.",
                "references_links": ["https://example.com/backup_vulnerability"],
                "cvss_version": "3.1",
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
                "cvss_base_score": 5.3,
            }
        ],
    }

    links = [
        {
            "link": data["1"]["url"],
            "id": 1,
            "is_active": id == 1,
        },
        {
            "link": data["2"]["url"],
            "id": 2,
            "is_active": id == 2,
        },
        {
            "link": data["3"]["url"],
            "id": 3,
            "is_active": id == 3,
        },
        {
            "link": data["4"]["url"],
            "id": 4,
            "is_active": id == 4,
        },
    ]

    target = {
        "website": data[str(id)]["url"],
        "vulnerabilities": data_vul[str(id)],
    }
    # results = ScannerMasterResult.objects.filter(target_id=id)
    # for r in results:
    #     links.append(
    #         {
    #             "link": r.url,
    #             "id": r.id,
    #             "is_active": r.id == tab_active,
    #         }
    #     )

    # context = {
    #     "links": links,
    #     "target": {
    #         "website": data[ta],
    #         "id": target.id,
    #         "vulnerabilities": ScannerMasterResultSerializer(instance=results, many=True).data,
    #     },
    # }

    context = {
        "links": links,
        "target": target,
    }

    return render(request, "detail.html", context)
