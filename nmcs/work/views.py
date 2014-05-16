from django.shortcuts import render

# Create your views here.


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
    frameTable3 = Frame(x1=0*inch, y1=2.0*inch, width=8.5*inch, height=4.25*inch)

    frameTable4 = Frame(x1=0.0*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch)
    frameTable5 = Frame(x1=4.25*inch, y1=0.7*inch, width=4.25*inch, height=1.3*inch)


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

    #serviceprotocol = Serviceprotocol.objects.get(pk=kwargs.get('pk', None))

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
    data = [['Datum:', '5/5/2014']]
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
    foo = 'Blablabla bla bla blall bllalall bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal Blablabla bla bla blall bllalall bla bal bla bal bla b !MAX 4 RADER!'
    bar = 'Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar Foo Bar foobar foobar fo bar fofofo bar fo bar fofofo bar !MAX 4 RADER!'

    p1 = Paragraph("%s" % foo, styleSheet["BodyText"])
    p2 = Paragraph("%s" % bar, styleSheet["BodyText"])

    data = [['Kund:', 'Kalle Anka'],
            ['Adress:', 'Drabantgatan 22 A'],
            ['Telefon:', '0767774164'],
            ['Mc:', 'Harley Davidsson aa'],
            ['Modell:', 'TRIUMPH CIVIC'],
            ['År:', '2014'],
            ['Motor:', 'NXT-3 AA4'],
            ['Arbete:', p1],
            ['Anm:', p2],
            ['Regnr:', 'ABC123'],
            ['Km:', '9999']]

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
    d._argW[2]=3.5*inch
    d._argW[3]=1.0*inch
    d._argW[4]=1.0*inch

    elements.append(d)


    #For varje artikel lagg till rad med information
    #MAX 15 articles
    counter = 0
    for articles in range(10):
        counter += 1
        data = [['', '', '', '', '']]
        e=Table(data,style=[        #(col, row)
                            ('GRID',(0,0),(-1,-1),2,colors.black),
                            ('ALIGN',(0,0),(-1,-1),'LEFT'),             
        ])
        e._argW[0]=1.0*inch
        e._argW[1]=1.0*inch
        e._argW[2]=3.5*inch
        e._argW[3]=1.0*inch
        e._argW[4]=1.0*inch

        elements.append(e)

    #Calculate how many empty rows to fill up
    rest = (15 - counter)
    for empty_articles in range(rest):
        data = [['', '', '', '', '']]
        e=Table(data,style=[        #(col, row)
                            ('GRID',(0,0),(-1,-1),2,colors.black),
                            ('ALIGN',(0,0),(-1,-1),'LEFT'),             
        ])
        e._argW[0]=1.0*inch
        e._argW[1]=1.0*inch
        e._argW[2]=3.5*inch
        e._argW[3]=1.0*inch
        e._argW[4]=1.0*inch

        elements.append(e)       

    elements.append(FrameBreak())
    ###############################################################

    ###############################################################
    #Anmarkning
    foo = "asfadf asdasd asd asdas sadsa d s dsd  s d sds ds sdsss sd sds ss sfadf asdasd asd asdas sadsa d s dsd  s d sds ds sdsss sd sds ss sfadf asdasd asd asdas sadsa d s dsd  s d sds ds !MAX 4 RADER!"

    p3 = Paragraph("%s" % foo, styleSheet["BodyText"])

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

    data = [['Fö. Matr..', ''],
            ['Summa', ''],
            ['Moms:', ''],
            ['Att betala:', '']]

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

