from django.urls import path

from .views import *


urlpatterns = [
    #the first for list are for people in the same university witb the vendoor
    #this is the list of items arranged according to their categories
    path('Item_list/<pk>/',Itemlist.as_view()),
    #this is just like the homepage
    path('fullitemlist/',fullItemlist),
    path('category_list/',category_list),
    #a list of the items owned by a vendor
    path('vendor_item_list/',vendorItemList),

    #The following show the list of items according to the user location ,the last two will show a list of food items of vendors in other locations
    path('marketplace/',marketplace_fullItemlist),
    path('marketplace/category/items/<id>/',marketplace_Itemlist),
    path('marketplace/other_locations/',marketplace_otherlocations),

    path('search/',search),
    path('university/search/',search_university),
    path('createitem/',createitem),
    path('updateitem/<id>/',updateitem),
    path('itemdetail/<id>/',itemdetail),
    path('view_vendor/<id>/',view_vendor),
    path('add_to_cart/<id>/',add_to_cart),
    path('remove_from_cart/<id>/',remove_from_cart),
    path('order_summary/',order_summary),
    #TOTAL PRICE OF THE ORDER
    path('order_total/',order_price),
    path('check_out/',checkout),

    #NOTE:FOR THE VENDOR. THIS LIST OF THE VENDORS ORDERED ITEMS
    path('ordered_items/',ordered_items),
    path('initiate_payment/',initiate_payment),
    path('verify_payment/',verify_payment),

]