from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=50, required=True, )
    clue_id = forms.IntegerField(required=True,widget = forms.HiddenInput(),)
