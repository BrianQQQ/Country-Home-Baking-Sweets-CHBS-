
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getToken('csrftoken');

function getCookie(name) {
    //Split cookie string and get all individual name=value pair in an array
    let cookieArr = document.cookie.split(";");

    //loop through the array elements 
    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");

        /*Removing whitespace at the beginning of the cookie name and
        compare it with the given string */
        if (name == cookiePair[0].trim()) {
            //Decode the cookie valye and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    //Return null if not found
    return null;
}
let cart = JSON.parse(getCookie('cart'))

if (cart == undefined) {
    cart = {}
    console.log('cart was created')
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

console.log('Cart;', cart)

let updateBtns = document.getElementsByClassName('update-cart')

// loops through add to cart buttons
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log(document.cookie)
        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

// add or remove an item from the cookie/guest user's Cart for unauthenticated user
function addCookieItem(productId, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('item should be deleted')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

// sends the data in json format and add or remove action to the view update_item from the users Cart for authenticated user
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    //stores the url to send the data
    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
            location.reload()
        });
}

function snack(productName) {
    console.log("working")
    // Get the snackbar DIV
    let x = document.getElementById("snackbar");

    x.innerText = productName + " added to cart"
    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}


function totalCount(name){
    let totalC = 0;
    let c = document.cookie.split(";")
    for (let i=0; i<c.length; i++){
        let elmnt = c[i].trim().split("=");
        if (elmnt[0] == name){
            let par = JSON.parse(decodeURIComponent(elmnt[1])); 
            for (let o in par){
                totalC += par[o]['quantity'];
            }
        }
    }

    document.getElementById("cart-quantity").innerText = totalC; 
}

document.addEventListener('DOMContentLoaded',  totalCount('cart'));