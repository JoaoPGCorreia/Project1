from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
from markdown2 import Markdown
from random import randint

class NewPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)

class EditPage(forms.Form):
    content = forms.CharField(label='content', widget=forms.Textarea)

# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "body_title": "All Pages",
        "entries": util.list_entries()
    })


def get_content(request, title): 
    md_content = util.get_entry(title)
    mk = Markdown()
    html_content = mk.convert(md_content)

    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": html_content
    })

def search_entry(request):
    entry = request.GET.get('q')

    try:
        md_content = util.get_entry(entry)
        mk = Markdown()
        html_content = mk.convert(md_content)

        return render(request, "encyclopedia/entries.html", {
            "title": entry,
            "content": html_content
        })

    except:
        similar_words = []
        list_entries = util.list_entries()

        for ent in list_entries:
            if entry in ent:
                similar_words.append(ent)

        if similar_words:
            return render(request, "encyclopedia/index.html", {
                "body_title": "Did you mean..",
                "entries": similar_words
            })

        else:
            return render(request, "encyclopedia/entries.html", {
                "entries": similar_words
            })

def create_new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            if util.get_entry(title):
                return render(request, "encyclopedia/entries.html", {
                    "exists": True 
                })

            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(f"wiki/{title}")

        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPage()
    })

def edit_page(request, title):
    md_content = util.get_entry(title)

    if request.method == "POST":
        form = EditPage(request.POST, initial={'content':md_content})
        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("content", kwargs={'title':title}))

        else:
            return render(request, "encyclopedia/new_page.html", {
                "edit": True,
                "md": md_content,
                "title": title,
                "form": form
            })

    return render(request, "encyclopedia/new_page.html", {
        "edit": True,
        "md": md_content,
        "title": title,
        "form": EditPage(initial={'content':md_content})
    })    

def random_page(request):
    all_pages = util.list_entries()

    page_index = randint(0, len(all_pages) - 1)

    title = all_pages[page_index]

    return HttpResponseRedirect(reverse("content", kwargs={'title':title}))