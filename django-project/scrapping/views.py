from django.shortcuts import render, redirect
from django.http import Http404

import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup

import os
import shutil

from .models import detailProduct

from .forms import LinkForm




# Create your views here.


def home(request) :

    form = LinkForm(request.POST or None)

    title = 'Home | Scrapping Product Fabelio'

    context = {
        'title' : title,
        'data_form' : form,
    }
    
    # print(request.POST)


    if request.method == 'POST':
        
        if form.is_valid():

            # linkScrapping = form.cleaned_data.get('input_Link'),
            # print(linkScrapping)

            print(request.POST['input_Link'])

            #request.session['input_Link'] = request.POST['input_Link']

            if 'input_Link' in request.POST:
                print("Come Herre")
                link_input = request.POST['input_Link']
                request.session['input_Link'] = link_input
            else:
                print("not here")
                link_input = False
    
            return redirect('scrapping-product/')

    return render(request,'scrapping/home.html', context)


def get_ListProduct (request) :
    
    title = 'List Produk Scrapping Fabelio'
    
    products = detailProduct.objects.all()
    
    context = {
        'title' : title,
        'products' : products, 
    }

    return render(request, "scrapping/list-product.html", context)


def detail_Product (request, my_id)  :
    
    try :
        products = detailProduct.objects.get(id=my_id)
    except detailProduct.DoesNotExist:
        raise Http404

    title = 'Detail Produk Fabelio'

    context = {
        'title' : title,
        'product_id' : products,
        
    }
    
    return render(request, "scrapping/detail.html", context)


def scrape(request) :

    _url = request.session.get('input_Link')
    
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    
    print("URL will Come")
    print(_url)

    print("yeeaaah good")
    #_url = "https://fabelio.com/ip/meja-kerja-clooney.html"

    if _url == "" :
        details = None
        print("")
    
    else :
        page = session.get(_url, verify = False)
        soup = BeautifulSoup(page.content, "html5lib")

        title = soup.find("span", {"data-ui-id": "page-title-wrapper"})
        price = soup.find("span", {"class" : "price" })
        description = soup.find("div", {"class" : "product-info__description"})
        

        # Scrapping Multiple Image and save image to local folder
        
        img_posts = soup.find_all('div', {'class' : 'fotorama__stage__frame'})
        
        print(len(img_posts))

        #name_image = []

        # for img_post in img_posts :
        #     image_source = soup.find("img", {"class" : "fotorama__img"})['data-src']

        #     media_root = 'D:\Project\Scrapping-Fabelio\media_root'
        #     if not image_source.startswith(("data:image", "javascript")) :
        #         local_filename = image_source.split('/')[-1].split("?")[0]
        #         name_image.append(local_filename)
        #         r = session.get(image_source, stream = True, verify = False)
        #         with open(local_filename, 'wb') as f :
        #             for chunk in r.iter_content(chunk_size=1024) :
        #                 f.write(chunk)
        #         current_image_absolute_path = os.path.abspath(local_filename)
        #         shutil.move(current_image_absolute_path, media_root)



        if title is not None and price is not None :

            url = _url
            title = title.get_text().strip()
            price = price.get_text()
            description = description.get_text().strip()
            # image_source1 = name[0]
            # image_source2 = name [1]
            # image_source3 = name [2]

            print(url)
            print(title)
            print(price)
            print(description)

            
            print("ready to store")
            new_product = detailProduct()
            
            new_product.url = url
            new_product.title = title
            new_product.price = price
            new_product.description = description
            # new_product.image1 = image_source1
            # new_product.image2 = image_source2
            # new_product.image3 = image_source3
            new_product.save()
            
            print("exiitt")

        else : 
            return None

    return redirect('scrapping:list')