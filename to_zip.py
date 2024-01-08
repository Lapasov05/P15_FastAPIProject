import os
import zipfile


async def create_zip(upload_file, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for foldername, filenames in os.walk(upload_file):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, upload_file)
                zipf.write(file_path, arcname)
