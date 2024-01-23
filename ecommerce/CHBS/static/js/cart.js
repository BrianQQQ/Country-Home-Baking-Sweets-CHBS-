// Author: Taiwo Akinlabi
// Code sourced from : https://www.youtube.com/watch?v=obZMr9URmVI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=2
var updateBtns = document.getElementsByClassName('update-cart')

// loops through add to cart buttons
for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

  // add or remove an item from the cookie/guest user's Cart for unauthenticated user
function addCookieItem(productId, action){
    console.log('User is not authenticated')

    if (action == 'add'){
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('item should be deleted')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

  // sends the data in json format and add or remove action to the view update_item from the users Cart for authenticated user
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

        //stores the url to send the data
        var url = '/update_item/'

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json', 
                'X-CSRFToken': csrftoken, 
            },
            body:JSON.stringify({'productId': productId, 'action': action})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
            location.reload()
        });
}