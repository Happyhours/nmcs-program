from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, DetailView

import decimal
# Create your views here.

from .models import (
    Workorder,
    Article
)

from .forms import ( 
    WorkorderForm,
    ArticleForm,
    ArticlesForm,
)

from customers.models import Customer


class WorkDetailView(DetailView):
    model = Workorder
    template_name = 'work/work_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)
        context['pk'] = self.object.pk

        articles = self.object.article_set.all()
        context['articles'] = articles
        context['workorder_calculations'] = self.object.workorder_calculations()

        return context


class WorkDeleteView(DeleteView):
    model = Workorder
    template_name = 'work/work_confirm_delete.html'


    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.pk})


def workUpdateView(request, *args, **kwargs):

    #Get in
    pk = kwargs.get('pk', None)
    workorder = kwargs.get('workorder', None)

    #Fetch initial data globaly in view
    customer = Customer.objects.get(pk=kwargs.get('pk', None))
    mc = customer.get_active_mc()

    #Data to return if there is a error in post and get is not called
    #Check if workorder has any articles
    workorder_tmp = Workorder.objects.get(pk=workorder)
    if workorder_tmp.article_set.all():
        #Populated listform for articles
        articles_form = ArticlesForm(workorder_tmp.pk, prefix="articles")
    else:
        #Empty listform for articles
        articles_form = ArticlesForm(prefix="articles")
    workorder_calculations = workorder_tmp.workorder_calculations()


    if request.method == 'POST':
        #POST
        #Get current intance of workorder and update it with data posted
        #workorder_tmp = Workorder.objects.get(pk=workorder)
        workorder_form = WorkorderForm(request.POST, instance=workorder_tmp, prefix='workorder')
        article_form = ArticleForm(request.POST, prefix='article')


        if 'add_article' in request.POST:
            #Add article to something

            if article_form.is_valid() and workorder_form.is_valid():
                
                workorder_model = workorder_form.save()

                article = article_form.save(commit=False)
                article.workorder = workorder_model
                article.price_total = article_form.cleaned_data['price'] * decimal.Decimal(article_form.cleaned_data['quantity'])
                article.save()

                #Also modify the real motorcykle and not only the form temporary values!
                mc.model.model = workorder_form.cleaned_data['model']
                mc.model.brand = workorder_form.cleaned_data['brand']
                mc.year = workorder_form.cleaned_data['year']
                mc.km = workorder_form.cleaned_data['km']
                mc.motor = workorder_form.cleaned_data['motor']
                mc.save()

                return HttpResponseRedirect(reverse('work-update', kwargs={'pk': pk,'workorder': workorder}))

            else:
                #Not valid forms
                pass


        if 'save_workorder' in request.POST:

            if workorder_form.is_valid():

                workorder_model = workorder_form.save(commit=False)
                #customer = Customer.objects.get(pk=kwargs.get('pk', None))
                workorder_model.customer = customer
                #workorder_model.registration_nr = mc.registration_nr
                workorder_model.save()  

                #Also modify the real motorcykle and not only the form temporary values!
                mc.model.model = workorder_form.cleaned_data['model']
                mc.model.brand = workorder_form.cleaned_data['brand']
                mc.year = workorder_form.cleaned_data['year']
                mc.km = workorder_form.cleaned_data['km']
                mc.motor = workorder_form.cleaned_data['motor']
                mc.save()

                return HttpResponseRedirect(reverse('work-detail', kwargs={'pk': workorder}))

            else:
                #Not valid forms
                pass  

        if 'remove_article' in request.POST:
            if 'articles-articles' in request.POST and workorder_form.is_valid():
                
                #Security vunability
                article_pk = int(request.POST.get('articles-articles', None))

                try: 
                    article = Article.objects.get(pk=request.POST.get('articles-articles', None))
                    article.delete()
                except Article.DoesNotExist:
                    pass

                workorder_model = workorder_form.save()

                #Also modify the real motorcykle and not only the form temporary values!
                mc.model.model = workorder_form.cleaned_data['model']
                mc.model.brand = workorder_form.cleaned_data['brand']
                mc.year = workorder_form.cleaned_data['year']
                mc.km = workorder_form.cleaned_data['km']
                mc.motor = workorder_form.cleaned_data['motor']
                mc.save()

                return HttpResponseRedirect(reverse('work-update', kwargs={'pk': pk,'workorder': workorder}))

    else:
        #GET
        workorder_model = Workorder.objects.get(pk=workorder)
        workorder_form = WorkorderForm(instance=workorder_model, prefix='workorder')
        #Form for creating a new article
        article_form = ArticleForm(prefix='article')

        #Check if workorder has any articles
        if workorder_model.article_set.all():
            #Populated listform for articles
            articles_form = ArticlesForm(workorder_model.pk, prefix="articles")
        else:
            #Empty listform for articles
            articles_form = ArticlesForm(prefix="articles")

        workorder_calculations = workorder_model.workorder_calculations()


    return render(request, 'work/work_update.html', 
        {'pk': pk, 
        'workorder_pk': workorder,
        'article_form': article_form,
        'workorder_form': workorder_form,
        'reg': mc.registration_nr,
        'articles_form': articles_form,
        'workorder_calculations': workorder_calculations
        })


def workCreateView(request, workorder=None, *args, **kwargs):

    #Fetch initial data globaly in view
    customer = Customer.objects.get(pk=kwargs.get('pk', None))
    mc = customer.get_active_mc()
    articles_form = ArticlesForm(prefix="articles")

    if request.method=='POST':

        if workorder == None:
            #If workorder does not exists
            article_form = ArticleForm(request.POST, prefix='article')
            workorder_form = WorkorderForm(request.POST, prefix='workorder')
            #workorder_calculations = self.object.workorder_calculations()
            #Default values if no articles
            cal = {}
            cal['sum'] = decimal.Decimal('0')
            expendables = decimal.Decimal('0')
            cal['expendables'] = expendables
            vat_percentage = decimal.Decimal('0')
            cal['vat'] = (cal['sum'] * vat_percentage)
            cal['total'] = (cal['sum'] * vat_percentage) + expendables
            workorder_calculations = cal
        else:
            #If workorder exists
            workorder_tmp = Workorder.objects.get(pk=workorder)
            workorder_form = WorkorderForm(request.POST, instance=workorder_tmp, prefix='workorder')
            article_form = ArticleForm(request.POST, prefix='article')

            workorder_calculations = workorder_tmp.workorder_calculations()

            #Check if customer has workorder has any articles
            if workorder_tmp.article_set.all():
                articles_form = ArticlesForm(workorder_tmp.pk, prefix="articles")

        if 'add_article' in request.POST:
            #Add article to something
            print('add_article, PRESSED')

            if workorder == None:
                #Workorder does not exist, create one.
                print("workorder == None")
                print(workorder_form.is_valid())
                print(workorder_form.errors)
                if article_form.is_valid() and workorder_form.is_valid():
                    #Both forms are valid
                    #print("Valid forms")

                    workorder_model = workorder_form.save(commit=False)
                    workorder_model.customer = None
                    workorder_model.registration_nr = mc.registration_nr
                    workorder_model.save()

                    article = article_form.save(commit=False)
                    article.workorder = workorder_model
                    article.price_total = article_form.cleaned_data['price'] * decimal.Decimal(article_form.cleaned_data['quantity'])
                    article.save()        

                    #Also modify the real motorcykle and not only the form temporary values!
                    mc.model.model = workorder_form.cleaned_data['model']
                    mc.model.brand = workorder_form.cleaned_data['brand']
                    mc.year = workorder_form.cleaned_data['year']
                    mc.km = workorder_form.cleaned_data['km']
                    mc.motor = workorder_form.cleaned_data['motor']
                    mc.save()
                    
                    ##Add workorder id to url and return to page with new url
                    pk = kwargs.get('pk', None)
                    return HttpResponseRedirect(reverse('work-create', kwargs={'pk': pk,'workorder': workorder_model.pk}))

                else:
                    #Not valid forms
                    print("NOT VALID FORMS")
                    pass

            else:
                #Workorder already exist add article to it.

                if article_form.is_valid() and workorder_form.is_valid():
                    
                    workorder_model = workorder_form.save()

                    article = article_form.save(commit=False)
                    article.workorder = workorder_model
                    article.price_total = article_form.cleaned_data['price'] * decimal.Decimal(article_form.cleaned_data['quantity'])
                    article.save()


                    #Also modify the real motorcykle and not only the form temporary values!
                    mc.model.model = workorder_form.cleaned_data['model']
                    mc.model.brand = workorder_form.cleaned_data['brand']
                    mc.year = workorder_form.cleaned_data['year']
                    mc.km = workorder_form.cleaned_data['km']
                    mc.motor = workorder_form.cleaned_data['motor']
                    mc.save()


                    ##Add workorder id to url and return to page with new url
                    pk = kwargs.get('pk', None)
                    return HttpResponseRedirect(reverse('work-create', kwargs={'pk': pk,'workorder': workorder_model.pk}))

                else:
                    #Not valid forms
                    #print("ARTICLE_FORM NOT VALID")
                    pass


        if 'save_workorder' in request.POST:
            #Save everything and connect customer to it
            #print('save_workorder, PRESSED')

            if workorder_form.is_valid():

                workorder_model = workorder_form.save(commit=False)
                #customer = Customer.objects.get(pk=kwargs.get('pk', None))
                workorder_model.customer = customer
                workorder_model.registration_nr = mc.registration_nr
                workorder_model.save()  

                #Also modify the real motorcykle and not only the form temporary values!
                mc.model.model = workorder_form.cleaned_data['model']
                mc.model.brand = workorder_form.cleaned_data['brand']
                mc.year = workorder_form.cleaned_data['year']
                mc.km = workorder_form.cleaned_data['km']
                mc.motor = workorder_form.cleaned_data['motor']
                mc.save()

                pk = kwargs.get('pk', None)

                return HttpResponseRedirect(reverse('customer-detail', kwargs={'pk': pk }))

            else:
                #Not valid forms
                #print("NOT VALID FORMS")
                #print("2")
                pass         



        if 'remove_article' in request.POST:
            #print('remove_article, PRESSED')
            if 'articles-articles' in request.POST and workorder_form.is_valid():

                article_pk = int(request.POST.get('articles-articles', None))

                try: 
                    article = Article.objects.get(pk=request.POST.get('articles-articles', None))
                    article.delete()
                except Article.DoesNotExist:
                    pass

                workorder_model = workorder_form.save()

                #Also modify the real motorcykle and not only the form temporary values!
                mc.model.model = workorder_form.cleaned_data['model']
                mc.model.brand = workorder_form.cleaned_data['brand']
                mc.year = workorder_form.cleaned_data['year']
                mc.km = workorder_form.cleaned_data['km']
                mc.motor = workorder_form.cleaned_data['motor']
                mc.save()

                pk = kwargs.get('pk', None)
                return HttpResponseRedirect(reverse('work-create', kwargs={'pk': pk,'workorder': workorder}))
                

    else:
        #GET
        if workorder != None:
            #If workorder exists
            workorder_model = Workorder.objects.get(pk=workorder)
            workorder_form = WorkorderForm(instance=workorder_model, prefix='workorder')
            article_form = ArticleForm(prefix='article')

            workorder_calculations = workorder_model.workorder_calculations()
            #Check if customer workorder has any articles
            if workorder_model.article_set.all():
                articles_form = ArticlesForm(workorder_model.pk, prefix="articles")
            else:
                articles_form = ArticlesForm(prefix="articles")

        else:
            #If workorder does not exist
            #workorder_calculations = self.object.workorder_calculations()

            workorder_calculations = {}

            #Default values if no articles
            cal = {}
            cal['sum'] = decimal.Decimal('0')
            expendables = decimal.Decimal('0')
            cal['expendables'] = expendables
            vat_percentage = decimal.Decimal('0')
            cal['vat'] = (cal['sum'] * vat_percentage)
            cal['total'] = (cal['sum'] * vat_percentage) + expendables
            workorder_calculations = cal

            articles_form = ArticlesForm(prefix="articles")
            article_form = ArticleForm(prefix='article')
            workorder_form = WorkorderForm(prefix='workorder', initial = {
                                                    'brand': mc.model.brand,
                                                    'model': mc.model.model,
                                                    'year': mc.year,
                                                    'km': mc.km,
                                                    'motor': mc.motor})
    print(workorder_calculations)
    return render(request, 'work/work_create.html', 
        {'pk': 1, 
        'article_form': article_form,
        'workorder_form': workorder_form,
        'reg': mc.registration_nr,
        'articles_form': articles_form,
        'workorder_calculations': workorder_calculations
        })


        #Check if the workorder for customer has any articles
        #if workorder.article_set.all():
            #context['articles_form'] = ArticlesForm(self.object.pk, prefix="articles")
        #else:
        #    context['articles_form'] = []


def some_view3(request, *args, **kwargs):

    from django.http import HttpResponse

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate, FrameBreak, Spacer
    from reportlab.lib.styles import getSampleStyleSheet


    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    #A4 width = 8.5 inches

    # define frames - for frames in page
    # frameHeader = Frame(x1=0*inch, y1=10.0*inch, width=8.5*inch, height=1.0*inch, showBoundary=1)


    # frameTable1 = Frame(x1=0.0*inch, y1=6.25*inch, width=3.8*inch, height=3.95*inch, showBoundary=1)
    # frameTable2 = Frame(x1=3.8*inch, y1=6.25*inch, width=4.7*inch, height=3.95*inch, showBoundary=1)

    # #Articles
    # frameTable3 = Frame(x1=0*inch, y1=2.0*inch, width=8.5*inch, height=4.25*inch, showBoundary=1)

    # frameTable4 = Frame(x1=0.0*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch, showBoundary=1)
    # frameTable5 = Frame(x1=4.25*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch, showBoundary=1)


    # frameTable6 = Frame(x1=0.4*inch, y1=0.0*inch, width=1.6*inch, height=0.7*inch, showBoundary=1)
    # frameTable7 = Frame(x1=2.0*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch, showBoundary=1)   
    # frameTable8 = Frame(x1=3.5*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch, showBoundary=1)
    # frameTable9 = Frame(x1=5.0*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch, showBoundary=1)   
    # frameTable10 = Frame(x1=6.5*inch, y1=0.0*inch, width=1.6*inch, height=0.7*inch, showBoundary=1)


    frameHeader = Frame(x1=0*inch, y1=10.0*inch, width=8.5*inch, height=1.0*inch,)


    frameTable1 = Frame(x1=0.0*inch, y1=6.25*inch, width=3.8*inch, height=3.95*inch)
    frameTable2 = Frame(x1=3.8*inch, y1=6.25*inch, width=4.7*inch, height=3.95*inch)

    #Articles
    frameTable3 = Frame(x1=0*inch, y1=2.0*inch, width=8.5*inch, height=4.50*inch)

    frameTable4 = Frame(x1=0.2*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch)
    frameTable5 = Frame(x1=4.48*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch)


    frameTable6 = Frame(x1=0.4*inch, y1=0.0*inch, width=1.6*inch, height=0.7*inch)
    frameTable7 = Frame(x1=2.0*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch)   
    frameTable8 = Frame(x1=3.5*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch)
    frameTable9 = Frame(x1=5.0*inch, y1=0.0*inch, width=1.5*inch, height=0.7*inch)   
    frameTable10 = Frame(x1=6.5*inch, y1=0.0*inch, width=1.6*inch, height=0.7*inch)

    #frameTable6 = Frame(x1=5.5625*inch, y1=7.0*inch, width=1.5*inch, height=1.0*inch)
    #Checkboxes
    #frameTable7 = Frame(x1=1.0625*inch, y1=1.5*inch, width=1.5*inch, height=6.2*inch)
    #frameTable8 = Frame(x1=2.5625*inch, y1=1.5*inch, width=5.5*inch, height=5.5*inch)
    #Signature
    #frameTable9 = Frame(x1=0*inch, y1=0.5*inch, width=8.5*inch, height=1.0*inch)


    # define pageTemplates - for page in document
    mainPage = PageTemplate(frames=[frameHeader, frameTable1, frameTable2,
                                    frameTable3, frameTable4, frameTable5,
                                    frameTable6, frameTable7, frameTable8,
                                    frameTable9, frameTable10
    ])

    # define BasicDocTemplate - for document
    doc = BaseDocTemplate(response, pagesize=letter, pageTemplates=mainPage)
    
    # styles
    styleSheet = getSampleStyleSheet()
    styleH = styleSheet['Heading1']

    # create a story
    # container for the 'Flowable' objects
    elements = []
    


    # Add all the flowables to different frames
    #elements.append(heading)
    #elements.append(FrameBreak())      # move to next frame   


    #TESTING FRAMES
    #Two Columns
    #frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1', showBoundary=1)
    #frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2', showBoundary=1)
    #doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])

    #I = Image('replogo.gif')
    #I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
    #I.drawWidth = 1.25*inch


    ###############################################################
    #Hamta modeller som kommer anvandas fran databasen

    workorder = Workorder.objects.get(pk=kwargs.get('pk', None))

    #Serviceprotocol.objects.get(pk=kwargs.get('pk', None))
    #print(Serviceprotocol) 
    #  for product in Product.objects.all():
    #   p = Paragraph("%s" % product.name, style)
    #   Catalog.append(p)
    #   s = Spacer(1, 0.25*inch)
    #   Catalog.append(s)
    # doc.build(Catalog) 


    ###############################################################

    ###############################################################
    #Rubrik

    h = Paragraph("""<para align=center spaceb=3><b>Arbetsorder</b></para>""", styleH)
     
    elements.append(h)

    g = Spacer(1, 0.05*inch)

    elements.append(g)

    ###############################################################

    ###############################################################
    #DATUM
    data = [['Datum:', workorder.date]]
    a=Table(data,style=[
                        #('BOX',(0,0),(-1,-1),2,colors.black),
                        ('LINEBELOW',(0,0),(1,0),1,colors.black),
                        ('ALIGN',(0,0),(0,0),'CENTER'),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    a._argW[-1]=1.1*inch
     
    elements.append(a)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #Company information

    data = [["Nilsson's MC Shop AB"],
            ['Industrigatan 48'],
            ['58277 Linköping'],
            ['Tel 013-141459'],
            ['Verkstad Mob. 072-7141471'],
            ['ESD 2012']]

    b=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(0,5),'CENTER'),
                        
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(b)
    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #Customer and motorcykle information
    #foo = 'Blablabla bla bla blall bllalall bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal bla bal bla b !MAX 4 RADER!'
    #bar = 'Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar fo bar fofofo bar !MAX 4 RADER!'



    p1 = Paragraph("%s" % workorder.job, styleSheet["BodyText"])
    p2 = Paragraph("%s" % workorder.notification, styleSheet["BodyText"])

    data = [['Kund:', workorder.customer.first_name + " " + workorder.customer.last_name],
            ['Adress:', workorder.customer.street],
            ['Telefon:', workorder.customer.telephone_set.all()[0]],
            ['Mc:', workorder.brand],
            ['Modell:', workorder.model],
            ['År:', workorder.year],
            ['Motor:', workorder.motor],
            ['Arbete:', p1],
            ['Anm:', p2],
            ['Regnr:', workorder.registration_nr],
            ['Km:', workorder.km]]

    c=Table(data,style=[        #(col, row)
                        #('GRID',(0,0),(-1,-1),2,colors.black),
                        #('LINEABOVE',(1,1),(1,1),1,colors.black),
                        #('LINEABOVE',(1,2),(1,2),1,colors.black),
                        #('LINEABOVE',(1,3),(1,3),1,colors.black),
                        #('LINEABOVE',(1,4),(1,4),1,colors.black),
                        ('VALIGN',(0,7),(0,8),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    c._argW[1]=3.7*inch

    elements.append(c)

    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #Articles

    data = [['Art.nr.', 'Antal', 'Benämning', 'Pris st', 'Pris']]

    d=Table(data,style=[        #(col, row)
                        ('GRID',(0,1),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),             
    ])
    d._argW[0]=1.0*inch
    d._argW[1]=1.0*inch
    d._argW[2]=3.0*inch
    d._argW[3]=1.0*inch
    d._argW[4]=1.0*inch

    elements.append(d)


    #For varje artikel lagg till rad med information
    #MAX 15 articles

    existing_articles = int(workorder.article_set.all().count())
    max_articles = 15
    #Check if workorder has any articles
     
    #counter = 0
    for article in workorder.article_set.all():
        #counter += 1
        data = [[article.article_nr, article.quantity, article.description, article.price, article.price_total ]]
        e=Table(data,style=[        #(col, row)
                            ('GRID',(0,0),(-1,-1),2,colors.black),
                            ('ALIGN',(0,0),(-1,-1),'LEFT'),             
        ])
        e._argW[0]=1.0*inch
        e._argW[1]=1.0*inch
        e._argW[2]=3.0*inch
        e._argW[3]=1.0*inch
        e._argW[4]=1.0*inch

        elements.append(e)

    #Calculate how many empty rows to fill up
    rest = (max_articles - existing_articles)
    for empty_articles in range(rest):
        data = [['', '', '', '', '']]
        e=Table(data,style=[        #(col, row)
                            ('GRID',(0,0),(-1,-1),2,colors.black),
                            ('ALIGN',(0,0),(-1,-1),'LEFT'),             
        ])
        e._argW[0]=1.0*inch
        e._argW[1]=1.0*inch
        e._argW[2]=3.0*inch
        e._argW[3]=1.0*inch
        e._argW[4]=1.0*inch

        elements.append(e)       

    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #Anmarkning
    #foo = "asfadf asdasd asd asdas sadsa d s dsd  s d sds ds sdsss sd sds ss sfadf asdasd asd asdas sadsa d s dsd  s d sds ds sdsss sd sds ss sfadf asdasd asd asdas sadsa d s dsd  s d sds ds !MAX 4 RADER!"

    p3 = Paragraph("%s" % workorder.comment, styleSheet["BodyText"])

    data = [['Anmärkning.'],
            [p3]]

    f=Table(data,style=[        #(col, row)
                        #('GRID',(0,1),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),             
    ])
    #f._argW[0]=1.0*inch
    f._argW[0]=3.3*inch

    elements.append(f)

    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #Summering

    cal = workorder.workorder_calculations()

    data = [['Fö. Matr..', cal['expendables']],
            ['Summa', cal['sum']],
            ['Moms:', cal['vat']],
            ['Att betala:', cal['total']]]

    g=Table(data,style=[        #(col, row)
                        ('GRID',(1,0),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    g._argW[1]=1.5*inch

    elements.append(g)

    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #

    data = [["Orgnnr."],
            ['556877-4938']]

    h=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),     
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(h)
    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #
    data = [["Momsregnn/VAT"],
            ['SE5568774938']]

    h=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),     
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(h)
    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #
    data = [["Bankgiro"],
            ['830-5682']]

    h=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),     
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(h)
    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #
    data = [["Tel.nr"],
            ['013-141458']]

    h=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),     
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(h)
    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #
    data = [["Faxnr."],
            ['013-141458']]

    h=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),     
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(h)
    ###############################################################


    # write the document to disk
    doc.build(elements)

    return response

