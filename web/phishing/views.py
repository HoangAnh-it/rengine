from django.shortcuts import render


def phishing(request):
    context = {
        "slug": None,
    }
    return render(request, "phishing/index.html", context)
