from django.shortcuts import render

def index(request):
    name = request.GET.get("name") or "world!" #add this line
    return render("Hello, "+name) #replace the word “world!” with the variable name

def index2(request, val1 = 0): #add the view function (index2)
 return render("value1 = "+str(val1))