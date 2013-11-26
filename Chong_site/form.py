from django import forms

class ContactForm(forms.Form):
    sender = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'onFocus':"if(this.value=='Name'){this.value=''};",}))
    email =forms.EmailField(widget=forms.TextInput(attrs={'onFocus':"if(this.value=='Email'){this.value=''};",}))
    subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'onFocus':"if(this.value=='Subject'){this.value=''};",}))
    message = forms.CharField(required=False,widget=forms.Textarea)


