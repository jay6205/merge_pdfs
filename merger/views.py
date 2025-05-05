import tempfile
import json

from django.shortcuts import render
from django.http import FileResponse
from PyPDF2 import PdfMerger
from .forms import PDFMergeForm


def merge_pdfs(request):
    if request.method == "POST":
        form = PDFMergeForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("pdfs")
            file_order = json.loads(request.POST.get("file_order", "[]"))

            file_map = {f.name: f for f in uploaded_files}
            ordered_files = [file_map[name] for name in file_order if name in file_map]

            merger = PdfMerger()
            for f in ordered_files:
                merger.append(f)

            merged_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            merger.write(merged_file)
            merger.close()
            merged_file.seek(0)

            return FileResponse(
                open(merged_file.name, "rb"), as_attachment=True, filename="merged.pdf"
            )

    else:
        form = PDFMergeForm()

    return render(request, "merger/merge.html", {"form": form})
