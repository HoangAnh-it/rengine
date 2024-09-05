from django.shortcuts import render


def phishing(request, slug):
    context = {
        "phishing_nav_active": True,
    }
    return render(request, "phishing.html", context)
