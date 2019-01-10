from django import forms

from booker.authorization import *

class UploadRosterForm(forms.Form):

    override = forms.BooleanField(required=False)
    file = forms.FileField()

    @staticmethod
    def handle_uploaded_file(file, override=False):
        print('handling file')
        if override:
            for stud in Student.objects.all():
                stud.delete()
        for line in file:
            email = line.decode('utf-8').strip()
            if not is_enrolled(email):
                Student.make(email)
