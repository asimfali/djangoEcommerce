from django.shortcuts import render


def test_view(req):
    return render(req, 'base.html', {})
