from django import forms

from .models import Workorder, Article

class WorkorderForm(forms.ModelForm):

    class Meta:
        model = Workorder
        fields = [
            'model',
            'year',
            'km',
            'motor', 
            'job',
            'notification',
            'comment',
        ]

class ArticleForm(forms.ModelForm):
    description = forms.CharField(
            max_length = 750,
            required=False,
            widget = forms.Textarea(
                           attrs={'rows': 6,
                                  'cols': 40,
                                  #'style': 'height: 1em;'
                                  })
        )
    class Meta:
        model = Article
        fields = [
            'article_nr',
            'quantity',
            'description',
            'price',
        ]


class ArticlesForm(forms.Form):
    articles = forms.ModelChoiceField(queryset=Workorder.objects.none(),
            required=False,
            empty_label=None,
            widget = forms.Select(attrs={'class': 'form-control', 'size': '15'})
    )

    def __init__(self, workorder_pk=None, *args, **kwargs):
        super(ArticlesForm, self).__init__(*args, **kwargs)
        if workorder_pk != None:
            workorder = Workorder.objects.get(pk=workorder_pk)
            articles = workorder.article_set.all()
            self.fields['articles'].queryset=articles


# class ServiceprotocolForm(forms.ModelForm):

#     additional = forms.CharField(
#             max_length = 750,
#             widget = forms.Textarea
#         )

#     comment = forms.CharField(
#             max_length = 750,
#             widget = forms.Textarea
#         )

#     class Meta:
#         model = Serviceprotocol
#         fields = [
#             'model',
#             'year',
#         ]