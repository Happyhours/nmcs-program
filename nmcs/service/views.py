from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, DetailView

# Create your views here.

from .models import (
    Serviceprotocol 
)

from .forms import ( 
    ServiceprotocolForm
)

from customers.models import Customer

#class ServiceCreateView(CreateView):

def TestCreateView(request, *args, **kwargs):
    return render(request, 'service/service_create.html', {})


class ServiceCreateView(CreateView):
    model = Serviceprotocol
    form_class = ServiceprotocolForm
    template_name = 'service/service_create.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = None

        customer = Customer.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        mc = customer.get_active_mc()
        self.initial = {'model': mc.model.model,
                        'year': mc.year,
                        'km': mc.km}

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, reg=mc.registration_nr))

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return reverse('customer-detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceCreateView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.kwargs.get(self.pk_url_kwarg, None)

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        customer = Customer.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        #Fetch motorcykle
        mc = customer.get_active_mc()
        self.object.registration_nr = mc.registration_nr
        self.object.customer = customer
        self.object.save()

        #Also modify the real motorcykle and not only the form temporary values!
        mc.model.model = self.object.model
        mc.year = self.object.year
        mc.km = self.object.km
        mc.save()

        

        return HttpResponseRedirect(self.get_success_url())


class ServiceUpdateView(UpdateView):
    model = Serviceprotocol
    form_class = ServiceprotocolForm
    template_name = 'service/service_update.html'

    def get_success_url(self):
        return reverse('service-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.object.pk

        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        #check if form has been modifed
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ServiceDetailView(DetailView):
    model = Serviceprotocol
    template_name = 'service/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.object.pk

        return context




class ServiceDeleteView(DeleteView):
    model = Serviceprotocol
    template_name = 'service/service_confirm_delete.html'


    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.pk})



def some_view(request, *args, **kwargs):
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Image
    from django.http import HttpResponse
    #Hack for printing it directly instead
    #from reportlab.pdfbase import pdfdoc
    #pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:false,bShrinkToFit:true}\);)>>'

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # Egna inställningar
    #p.setLineWidth(.6)
    #p.setFont('Helvetica', 12)

    #Rubrik
    p.setFont('Helvetica', 12)
    p.drawCentredString(230,750,'SERVICEPROTOKOLL')
    #p.drawString(230,750,'SERVICEPROTOKOLL')

    #Bild
    bild = 'path/to/bild'
    p.drawImage(bild, 230, 500, width=None, height=None)



    p.drawString(100, 100, "Hello world.")

    



    p.drawString(30,550,'OFFICIAL COMMUNIQUE')
    p.drawString(30,535,'OF ACME INDUSTRIES')
    p.drawString(500,550,"12/12/2010")
    p.line(480,547,580,547)
     
    p.drawString(275,525,'AMOUNT OWED:')
    p.drawString(500,525,"$1,000.00")
    p.line(378,523,580,523)
     
    p.drawString(30,503,'RECEIVED BY:')
    p.line(120,500,580,500)
    p.drawString(120,503,"JOHN DOE")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def some_view2(request, *args, **kwargs):

    from django.http import HttpResponse

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

    # A large collection of style sheets pre-made for us
    #from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    #styles = getSampleStyleSheet()


    #from reportlab.lib import styles
    #style = styles['Normal']
    # for product in Product.objects.all():
    #  for product in Product.objects.all():
    #   p = Paragraph("%s" % product.name, style)
    #   Catalog.append(p)
    #   s = Spacer(1, 0.25*inch)
    #   Catalog.append(s)
    # doc.build(Catalog)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

     
    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
     
    data= [['Modell', '01', '02', '03', '04'],
           ['År', '11', '12', '13', '14'],
           ['Km', '21', '22', '23', '24'],
           ['Tekniker', '31', '32', '33', '34']]
    t=Table(data,5*[0.4*inch], 4*[0.4*inch])
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
     
    elements.append(t)
    # write the document to disk
    doc.build(elements)


    return response


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
    frameHeader = Frame(x1=0*inch, y1=9.6*inch, width=8.5*inch, height=1.2*inch)
    frameTable1 = Frame(x1=0.3*inch, y1=8.0*inch, width=4.25*inch, height=1.6*inch)
    frameTable2 = Frame(x1=4.25*inch, y1=8.0*inch, width=4.25*inch, height=1.6*inch)
    
    frameTable3 = Frame(x1=1.0625*inch, y1=7.0*inch, width=1.5*inch, height=1.0*inch)
    frameTable4 = Frame(x1=2.5625*inch, y1=7.0*inch, width=1.5*inch, height=1.0*inch)   
    frameTable5 = Frame(x1=4.0625*inch, y1=7.0*inch, width=1.5*inch, height=1.0*inch)
    frameTable6 = Frame(x1=5.5625*inch, y1=7.0*inch, width=1.5*inch, height=1.0*inch)
    #Checkboxes
    frameTable7 = Frame(x1=1.0625*inch, y1=1.5*inch, width=1.5*inch, height=6.2*inch)
    frameTable8 = Frame(x1=2.5625*inch, y1=1.5*inch, width=5.5*inch, height=5.5*inch)
    #Signature
    frameTable9 = Frame(x1=0*inch, y1=0.5*inch, width=8.5*inch, height=1.0*inch)


    # define pageTemplates - for page in document
    mainPage = PageTemplate(frames=[frameHeader, frameTable1, frameTable2,
                                    frameTable3, frameTable4, frameTable5,
                                    frameTable6, frameTable7, frameTable8,
                                    frameTable9
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

    serviceprotocol = Serviceprotocol.objects.get(pk=kwargs.get('pk', None))

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

    h = Paragraph("""<para align=center spaceb=3><b>Serviceprotocol</b></para>""", styleH)
     
    elements.append(h)

    g = Spacer(1, 0.25*inch)

    elements.append(g)

    ###############################################################

    ###############################################################
    #DATUM
    data = [['Datum:', '5/5/2014']]
    a=Table(data,style=[
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(0,0),'CENTER'),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    a._argW[-1]=1.1*inch
     
    elements.append(a)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #Modell, Ar, Km etc
    data = [['Modell:', serviceprotocol.model],
            ['År:', serviceprotocol.year],
            ['Km:', serviceprotocol.km],
            ['Tekniker:', serviceprotocol.employee],
            ['Regnr:', serviceprotocol.registration_nr]]
    b=Table(data,style=[        #(col, row)
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('LINEABOVE',(0,1),(1,1),1,colors.black),
                        ('LINEABOVE',(0,2),(1,2),1,colors.black),
                        ('LINEABOVE',(0,3),(1,3),1,colors.black),
                        ('LINEABOVE',(0,4),(1,4),1,colors.black),
                        ('ALIGN',(1,0),(1,4),'CENTER'),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    b._argW[1]=1.6*inch

    elements.append(b)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #Company information

    data = [["Nilsson's MC Shop AB"],
            ['Industrigatan 48'],
            ['58277 Linköping'],
            ['Tel 013-141459'],
            ['Mob. 072-7141471']]

    f=Table(data,style=[        #(col, row)
                        ('ALIGN',(0,0),(0,4),'CENTER'),
                        
    ])
    #f._argW[0]=1.6*inch
    
    
    elements.append(f)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #CHECKBOXES
    service_fields = [
                    'oil_check',
                    'motor_check',
                    'primary_check',
                    'gearbox_check',
                    'chain_check',
                    'cylinder_check',
                    'brakes_check',
                    'front_check',
                    'back_check',
                    'plug_check',
                    'rm_plug_check',
                    'grease_check',
                    'air_check',
                    'rm_air_check',
                    'filter_check',
                    'belt_check',
                    'tires_check',
                    'pressure_check',
                    'fuel_check',
                    'layer_check',
                    'rm_layer_check',
                    'support_check',
                    'blinkers_check',
                    'error_check',
    ]

    for field in service_fields:
        data = [['', field]]
        c=Table(data, 1*[0.3*inch], 1*[0.3*inch])
        LIST_STYLE = TableStyle([
                            ('BOX',(0,0),(0,0),2,colors.black),
                            ('ALIGN',(0,0),(0,0),'LEFT'),
                    ])
        #Modefiera celler i efterhand.
        if getattr(serviceprotocol,field) == True:
            LIST_STYLE.add('BACKGROUND',(0,0),(0,0),colors.black)
        #Lagg till allt
        c.setStyle(LIST_STYLE)
        #Satt width pa column 1 till 1*inch
        c._argW[1]=1*inch
        #Lagg till i flow

        if field == 'oil_check' or field == 'motor_check' or field == 'primary_check' or field =='gearbox_check':
            elements.append(c)
            elements.append(FrameBreak())
        else:
            elements.append(c)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #Additional, Comments

    p1 = Paragraph("%s" % serviceprotocol.additional, styleSheet["BodyText"])
    p2 = Paragraph("%s" % serviceprotocol.comment, styleSheet["BodyText"])

    # data = [['Övrigt enl. önskemål:', p1],
    #         ['Anm:', p2]]

    # d=Table(data,style=[    #(col, row)
    #                     ('ALIGN',(0,0),(0,1),'RIGHT'),
    #                     ('VALIGN',(0,0),(0,1),'TOP'),
    #                     ('BOX',(0,0),(-1,-1),2,colors.black),
    #                     ('GRID',(0,0),(-1,-1),0.5,colors.green),
                        
    # ])
    # d._argW[0]=1.5*inch    

    data = [['Övrigt enl. önskemål:'],
            [p1],
            ['Anm:'],
            [p2],
    ]
    d=Table(data,style=[    #(col, row)
                        #('ALIGN',(0,0),(0,1),'RIGHT'),
                        #('VALIGN',(0,0),(0,1),'TOP'),
                        ('BOX',(0,0),(0,1),1.0,colors.black),
                        ('BOX',(0,2),(0,3),1.0,colors.black),
    ])
    d._argW[0]=4.8*inch
     
    elements.append(d)
    elements.append(FrameBreak())

    ###############################################################

    ###############################################################
    #Signature


    data = [['Signatur tekniker:', '']]
    e=Table(data,colWidths=None, rowHeights=1*[0.4*inch],style=[
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        
    ])
    e._argW[-1]=2.8*inch

    k = Spacer(1, 0.35*inch)
    elements.append(k)

    elements.append(e)

    ###############################################################


    # write the document to disk
    doc.build(elements)

    return response




