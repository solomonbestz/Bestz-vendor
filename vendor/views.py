from django.shortcuts import render,get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .serializers import ItemSerializer,CategorySerializer,HomeSerializer,OrderSerializer,OrderItemSerializer,itemserializer
from .models import *
from core.models import User
from collections import namedtuple
import requests
from core.serializers import registrationserializer
# Create youggggggr views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createitem(request):
    category=Category.objects.get(id=request.data["category"])
    data = {"quick":"silver"}
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save(vendor=request.user,category=category)
        data["message"] = "Item was created successfully"
        data["title"] = item.title
        data["price"] = item.price
        data["category"]=item.category.title
        return Response(data,status=status.HTTP_201_CREATED)


    else:
        data = serializer.errors

        return Response(data,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def updateitem(request,id):
    item=Item.objects.get(id=id,vendor=request.user)
    data = {"quick":"silver"}
    serializer = ItemSerializer(instance=item,data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        data["message"] = "Item was updated successfully"
        data["title"] = item.title
        data["price"] = item.price
        data["category"]=item.category.title
        return Response(data,status=status.HTTP_201_CREATED)


    else:
        data = serializer.errors

        return Response(data,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def itemdetail(request,id):
    item=Item.objects.get(id=id)
    data = {"quick":"silver"}
    serializer = ItemSerializer(item,many=False)


    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def search(request):
    item=Item.objects.filter(title__contains=request.data['search']).order_by('vendor__location')
    data = {"quick":"silver"}
    serializer = ItemSerializer(item,many=True)


    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def search_university(request):
    item=Item.objects.filter(vendor__university=request.user.university,title__contains=request.data['search'])
    data = {"quick":"silver"}
    serializer = ItemSerializer(item,many=True)


    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def item_delete(request,id):
    item=Item.objects.get(id=id)
    data = {"message":"ITEM HAS BEEN DELETED"}

    item.delete()

    return Response(data,status=status.HTTP_200_OK)


#NOT YET TESTED
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def view_vendor(request,id):
    item=Item.objects.get(id=id)
    print(item.vendor.vendor_name)
    user=User.objects.get(vendor_name=item.vendor.vendor_name)

    serializer =registrationserializer(user,many=False)


    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def category_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 3
    categories=paginator.paginate_queryset(Category.objects.all(),request)
    serializer=CategorySerializer(categories,many=True)

    return paginator.get_paginated_response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def fullItemlist(request):
    if request.user.university is None :
        data={"message":"you are not in any uni"}
        return Response(data)

    else:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        Home = namedtuple('Home', ('categories', 'items'))

        home=Home(
        categories=Category.objects.all(),
        items=paginator.paginate_queryset(Item.objects.filter(vendor__university=request.user.university).exclude(vendor=request.user), request))

        serializer=HomeSerializer(home)

        return paginator.get_paginated_response(serializer.data)


#NOT YET TESTED
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def marketplace_fullItemlist(request):

    paginator = PageNumberPagination()
    paginator.page_size = 10
    Home = namedtuple('Home', ('categories', 'items'))

    home=Home(
    categories=Category.objects.all(),
    items=paginator.paginate_queryset(Item.objects.filter(vendor__location=request.user.location).exclude(vendor=request.user), request))

    serializer=HomeSerializer(home)

    return paginator.get_paginated_response(serializer.data)

#NOT TESTED YET
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def marketplace_Itemlist(request,id):

    paginator = PageNumberPagination()
    paginator.page_size = 10

    items=paginator.paginate_queryset(Item.objects.filter(vendor__location=request.user.location,category__id=id).exclude(vendor=request.user), request)

    serializer=ItemSerializer(items,many=True)
    print(serializer.data)

    return paginator.get_paginated_response(serializer.data)#NOT TESTED YET

#NOT TESTED
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def marketplace_otherlocations(request):

    paginator = PageNumberPagination()
    paginator.page_size = 10
    items=paginator.paginate_queryset(Item.objects.all().order_by('vendor__location'), request)

    serializer=ItemSerializer(items,many=True)

    return paginator.get_paginated_response(serializer.data)#NOT TESTED YET@api_view(["POST"])

#NOT TESTED
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def marketplace_otherlocations_category(request,id):

    paginator = PageNumberPagination()
    paginator.page_size = 3

    items=paginator.paginate_queryset(Item.objects.filter(category__id=id).order_by('vendor__location'), request)

    serializer=ItemSerializer(items,many=True)

    return paginator.get_paginated_response(serializer.data)#NOT TESTED YET



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def vendorItemList(request):

    paginator = PageNumberPagination()
    paginator.page_size = 3
    items=paginator.paginate_queryset(Item.objects.filter(vendor=request.user),request)
    serializer=ItemSerializer(items,many=True)

    return  paginator.get_paginated_response(serializer.data)


class Itemlist(ListAPIView):
    serializer_class=ItemSerializer
    authentication_classes=([TokenAuthentication])
    permission_classes=([IsAuthenticated])

    def get_queryset(self):
        item=Item.objects.filter(category_id=self.request.resolver_match.kwargs['pk'],vendor__university=self.request.user.university).exclude(vendor=self.request.user)
        return item



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_to_cart(request,id):
    data={}
    item=get_object_or_404(Item, id=id)
    print(item.vendor.vendor_name)
    user=User.objects.get(vendor_name=item.vendor.vendor_name)
    print(user.email)
    order_item,created=OrderItem.objects.get_or_create(item=item,vendor=user,is_removed=False,user=request.user,is_ordered=False )
    print ("ok")

    order_qs=Order.objects.filter(user=request.user,is_ordered=False)
    print ("ok")
    if order_qs:
        order=order_qs[0]
        if order.items.filter(item__id=item.id):
            order_item.quantity+=1
            order_item.save()
            data["message"]="ITEM HAS BEEN INCREASED"
        else:
            order.items.add(order_item)
            data["message"] = "ITEM HAS BEEN ADDED TO CART"

    else:
        order=Order.objects.create(user=request.user)
        order.items.add(order_item)

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def remove_from_cart(request,id):
    data = {}
    item = get_object_or_404(Item, id=id)
    user=User.objects.get(vendor_name=item.vendor.vendor_name)


    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    print("ok")
    if order_qs:
        order = order_qs[0]
        if order.items.filter(item__id=item.id):
            order_item = OrderItem.objects.filter (item=item, vendor=user, user=request.user,
                                                                  is_ordered=False,is_removed=False)[0]
            order_item.is_removed=True
            order_item.save()
            order.items.remove(order_item)
            data["message"] = "ITEM HAS BEEN REMOVED"
        else:

            data["message"] = "ORDER DOESN'T HAVE THE ITEM"
    else:
        data["message"] = "USER DOES NOT HAVE AN ORDER"

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def order_summary(request):
    order=Order.objects.get(user=request.user,is_ordered=False,)
    #print(bok.author.all())
    serializer=OrderSerializer(order)
    return  Response (serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ordered_items(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    order=paginator.paginate_queryset(OrderItem.objects.filter(vendor=request.user,is_ordered=True,is_removed=False),request)
    #print(bok.author.all())
    serializer=OrderItemSerializer(order,many=True)
    return  paginator.get_paginated_response (serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def order_price(request):
    data={}
    order=Order.objects.get(user=request.user,is_ordered=False)
    #print(bok.author.all())
    data["TOTAL PRICE"]=order.get_total()
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def checkout(request):
    data={}
    print(request.data.get("delivery_location"))
    if request.data.get("delivery_location") == "school":
        print(request.user.university)
        order=Order.objects.get(user=request.user,is_ordered=False)
        order.delivery_location=request.user.university
        order.save()

    elif request.data.get("delivery_location")== "address":
        order=Order.objects.get(user=request.user,is_ordered=False)
        order.delivery_location=request.user.address
        order.save()

    else:
        order = Order.objects.get(user=request.user, is_ordered=False)
        order.delivery_location = request.data.get("delivery_location")
        order.save()

    for orderitems in order.items.all():
        orderitems.delivery_location=order.delivery_location
        orderitems.save()

    data["DELIVERY LOCATION"]=order.delivery_location
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def initiate_payment(request):
    data={}
    SECRET_KEY="sk_test_7731c88b0b5e13e70f73211704179bd06f354efe"
    payment=Payment(amount=500,email="rcabiodun@gmail.com",user=request.user)
    payment.save()
    order=Order.objects.get(is_ordered=False,user=request.user)
    order.ref=payment.ref
    order.save()
    payment.amount=order.get_total()
    payment.save()
    base_url='https://api.paystack.co'
    path='/transaction/initialize/'
    headers= {
        "Authorization" : 'Bearer sk_test_7731c88b0b5e13e70f73211704179bd06f354efe',
        'Content-Type': 'application/json'
    }
    body={"email":payment.email,"amount":payment.amount_value(),"reference":payment.ref,"callback_url":"http://127.0.0.1:8000/vendor/verify_payment"}
    url=base_url + path
    response=requests.post(url,headers=headers,json=body)
    print(response.json())
    checkout=(response.json())
    data["message"]="PAYMENT CREATED"
    return Response(checkout['data'])

def verify_payment(request):
    print(request.GET.get('reference'))
    order=Order.objects.get(ref=request.GET.get('reference'))
    context={"order":order}
    return render(request,'vendor/payment_confirmation.html',context)


