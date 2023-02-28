from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import pika, json, re, math

from .forms import UploadFileForm
from .models import Products, Receipts, ReceiptProcessingLogs, ReceiptsContent

def index(request):
    """The home page for nutrition project"""
    receipts = Receipts.objects.order_by('receipt_id')
    arr = upload_file_form(request)

    context = {'receipts': receipts, 'form': arr['form'], 'receipt_id': arr['receipt_id']}
    return render(request, 'ui_app/index.html', context)


def receipt(request, receipt_id):
    """Nutrition information for specific receipt"""
    products = ReceiptsContent.objects.all().filter(receipt_id = receipt_id).select_related("product")
    pcf = count_totals(products)
    context = {'products': products, 'pcf': pcf}
    return render(request, 'ui_app/receipt.html', context)

def count_totals(products):
    """What PFC a day we have as a result"""
    energy = 0
    fat = 0
    carbohydrate = 0
    protein = 0
    for product in products:
        energy += product.product.energy
        fat += product.product.fat
        carbohydrate += product.product.carbohydrate
        protein += product.product.protein
    
    # Calculations are based on the following suggestions:
    # There are 3 people in the family and products are purchased once a week
    # we have data in kgs and for 100g == 10

    energy = math.ceil(energy * product.quantity * 10 /3 /7)
    fat = math.ceil(fat * product.quantity * 10 /3 /7)
    carbohydrate = math.ceil(carbohydrate * product.quantity * 10 /3 /7)
    protein = math.ceil(protein * product.quantity * 10 /3 /7)

    p = math.ceil((protein * 4 * 100) / energy) 
    f = math.ceil((fat * 9 * 100) / energy)
    c = math.ceil((carbohydrate * 3.75 * 100) / energy)
    ratio = f"{c}:{f}:{p}"

    return {'quantity': product.quantity, 'energy': energy, 'fat': fat, 'carbohydrate': carbohydrate, 'protein': protein, 'ratio': ratio}


def upload_file_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("request_method is post")
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():  
            handle_uploaded_file(request.FILES['file'])
            receipt_id = save_file_to_db(request.FILES['file'])
            update_logs_table(receipt_id, 'The receipt name has been stored to DB')
            send_message_to_queue(receipt_id, request.FILES['file'])
            return {'form': '', 'receipt_id': receipt_id, 'file': request.FILES['file']} 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()
        receipt_id = ''

    return {'form': form, 'receipt_id': receipt_id}

def handle_uploaded_file(file):
    with open('ui_app/media/'+file.name, 'wb+') as destination:  
        for chunk in file.chunks():  
            destination.write(chunk)


def save_file_to_db(file):
    print('save receipt to db')
    receipt = Receipts()
    receipt.receipt_name = file
    receipt.date = ''
    receipt.save()
    return receipt.pk

def update_logs_table(receipt_id, message):
    print('save log')
    receipt = Receipts()
    receipt.receipt_id = receipt_id
    print('receipt_id', receipt_id)
    log = ReceiptProcessingLogs()
    log.receipt = receipt
    log.message = message
    log.save()
    return log.pk

def send_message_to_queue(receipt_id, file):

    file_name = str(file)
    data = {'receipt_id': receipt_id, 'file_name': file_name}
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(settings.MQ_HOSTNAME))
    channel = connection.channel()
    channel.queue_declare(queue='received_new_pdf')
    channel.basic_publish(exchange='', routing_key='received_new_pdf', body=json.dumps(data))
    print(" [x] Sent 'Hello World!'")
    connection.close()


@csrf_exempt
def api(request, receipt_id):
    #cheese_blog = Blog.objects.get(name="Cheddar Talk")
    messages = ReceiptProcessingLogs.objects.all().filter(receipt_id=receipt_id)
    saved = 0
    retreived = 0
    all_products = 0
    for message in messages:
        if(re.search('saved', message.message)):
            saved += 1
        elif(re.search('nutrition', message.message)):
            retreived += 1
        elif(re.search('All products', message.message)):
            all_products += 1

    if saved == retreived and all_products == 1:
        status = 'completed'
    else:
        status = 'in progress' 

    print(f'status: {status}, saved: {saved}, retreived: {retreived}')
    responce = {
        'receipt_id': receipt_id,
        'status': status,
        'saved': saved,
        'retreived': retreived
    }
    return JsonResponse(responce, safe=False)



