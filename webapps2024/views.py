from django.http import FileResponse


def serve_file(request, filename):
    file_path = 'webapps2024/static/' + filename
    return FileResponse(open(file_path, 'rb'))
