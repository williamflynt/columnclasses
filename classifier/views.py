import csv
import json
import random

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from classifier.forms import SourceUploadForm
from classifier.models import Classification, Source, Column


class ClassifyView(TemplateView):
    """display some CSVs for column classification"""

    template_name = "classifier/classify.html"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        src_id = random.choice(
            Source.objects.filter(time_classified=None).values_list("id", flat=True)
        )
        source = Source.objects.get(id=src_id)
        context["source"] = source
        with source.document.open("r") as f:
            reader = csv.reader(f, delimiter=",")
            lines = list(reader)
            context["headers"] = lines.pop(0)
            context["rows"] = lines[:5]
        mains = Classification.objects.filter(main=True).values_list("id", "label")
        context["mains"] = mains
        return context

    def get(self, request, *args, **kwargs):
        if Source.objects.filter(time_classified=None).count() > 0:
            return super().get(request, *args, **kwargs)
        else:
            messages.info(request, "Upload some files to get started!")
            return redirect(reverse_lazy("classify-home:upload-files"))

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        source = Source.objects.get(id=body.pop("sourceId"))
        for k, v in body.items():
            main = Classification.objects.get(id=v["main"]) if v.get("main") else None
            sub = Classification.objects.get(id=v["sub"]) if v.get("sub") else None
            Column.objects.create(
                source=source, index=k, main_class=main, sub_class=sub
            )
        messages.success(request, "Classified successfully!")
        source.time_classified = timezone.now()
        source.save()
        return JsonResponse(
            status=200, data={"location": reverse_lazy("classify:classify")}
        )


class LoadSubsView(View):
    """AJAX loader for subclassifications"""

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """get the subclassifications for a given main classification"""
        body = json.loads(request.body.decode("utf-8"))
        parent_id = body.get("id")
        subs = (
            Classification.objects.get(id=parent_id)
            .subclasses.all()
            .order_by("label")
            .values_list("id", "label")
        )
        subs = {c[0]: c[1] for c in subs}
        return JsonResponse(data=subs)


class SourceUploadView(FormView):
    form_class = SourceUploadForm
    template_name = "classifier/upload.html"
    success_url = reverse_lazy("classify:classify")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("document")
        if form.is_valid():
            sources = []
            for f in files:
                sources.append(Source(document=f))
            Source.objects.bulk_create(sources)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
