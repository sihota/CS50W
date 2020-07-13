from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


#class inherits from form.Forms
#inside class define fields to this form
#https://docs.djangoproject.com/en/3.0/ref/forms/fields/
#https://djangobook.com/mdj2-django-forms/
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    #priorty = forms.IntegerField(label = "Priority", initial = 1, min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html",{
        "tasks":request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        # create form with submitted post data
        form = NewTaskForm(request.POST)
        #https://docs.djangoproject.com/en/3.0/ref/forms/api/
        # check form input data is valid
        if form.is_valid():
            #cleaned_data attribute will include a key and value for all its fields#
            #If your data does not validate, the cleaned_data dictionary contains only the valid fields:
            # form.cleaned_date holds dictionary like this {'task':'entered task','priority':1}
            task = form.cleaned_data["task"]
            #tasks.append(task)
            request.session["tasks"] += [task]
            #add succesfully redirect
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request,"tasks/add.html",{
                "form": form
            })

    return render(request, "tasks/add.html",{
        "form":NewTaskForm()
    })
