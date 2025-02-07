from django.shortcuts import render, HttpResponse


def authoriz_moment(request):

    return render(request, "authorization/html/index.html")

