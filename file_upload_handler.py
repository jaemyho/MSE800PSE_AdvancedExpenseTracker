import os
from flask import request
from werkzeug.utils import secure_filename


class FileUploadHandler:
    def __init__(self, request, upload_folder):
        self.request = request
        self.upload_folder = upload_folder
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}  # Allowed file extensions

    def allowed_file(self, filename):
        """Check if the uploaded file has an allowed extension."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def handle_upload(self):
        """Handle the file upload process."""
        # Check if the file part is in the request
        if 'file' not in self.request.files:
            return None, "No file part"

        file = self.request.files['file']

        # If the user does not select a file, the browser submits an empty part without a filename
        if file.filename == '':
            return None, "No selected file"

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure the filename
            filepath = os.path.join(self.upload_folder, filename)

            # Save the file to the specified upload folder
            file.save(filepath)
            return filepath, None  # Return the filepath if successful

        return None, "File type not allowed"  # Return error if file type is not allowed
