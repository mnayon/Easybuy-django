from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from carts.models import Cartitem
from store.models import Product, Variation
from .models import Cart, Cartitem
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 



def add_cart(request, product_id):

    
    if request.method == 'POST':
        product = Product.objects.get(id = product_id)
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
    
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    try:
        cart_item = Cartitem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(

            product=  product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
 

    return redirect('carts')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = Cartitem.objects.get(cart = cart, product= product)

    if cart_item.quantity >1:
        cart_item.quantity -= 1
    

        cart_item.save()
    else:
        cart_item.delete
    
    return redirect('carts')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = Cartitem.objects.get(product= product, cart = cart)

    cart_item.delete()

    return redirect('carts')




def carts(request,total = 0, quantity = 0, cart_item = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = Cartitem.objects.filter(cart = cart , is_active = True)

        for cart_item in cart_items:
            
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }



    return render(request, 'store/carts.html',context)
 
  