from django.shortcuts import render


def index (request) :

    title = 'Index | Scrapping Product Fabelio'

    context = {
        title : title,
    }


    return render(request, "dashboard/index.html", context)