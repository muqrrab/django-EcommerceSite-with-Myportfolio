headercart();

if (
  window.location.href.indexOf("cart") > -1 ||
  window.location.href.indexOf("") > -1
) {
  cartpage();
}

var updateBtns = document.getElementsByClassName("update-cart");
for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    if (user === "AnonymousUser") {
      addcookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addcart(dataproduct) {
  var element = document.getElementById("updatecartadd");
  var productId = dataproduct;
  var action = element.getAttribute("data-action");
  if (user === "AnonymousUser") {
    addcookieItem(productId, action);
  } else {
    updateUserOrder(productId, action);
  }
}

function removecart(dataproduct) {
  var element = document.getElementById("updatecartremove");
  var productId = dataproduct;
  var action = element.getAttribute("data-action");
  if (user == "AnonymousUser") {
    addcookieItem(productId, action);
  } else {
    updateUserOrder(productId, action);
  }
}

function addcookieItem(productId, action) {
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      delete cart[productId];
    }
  }
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  headercart();
  cartpageoff();
  cartpage();
}

function updateUserOrder(productId, action) {
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      headercart();
      cartpageoff();
      cartpage();
    });
}

// BY Me ajax
function headercart() {
  $.ajax({
    url: "/header_cart",
    type: "GET",
    dataType: "json",
    success: function (item) {
      $("#headercart").html(
        '<div class="dropdown cart-dropdown">\
      <a href="/cart/" class="dropdown-toggle" role="button">\
          <div class="icon">\
              <i class="icon-shopping-cart" style="font-size:30px; margin-right:5px;"></i>\
              <span class="cart-count">'+item[0]+'</span>\
          </div>\
      </a>\
  </div>\
  <span class="cart-txt" style="margin-left:10px ;"> Rs. ' +
          item[1] +'</span></div>');
    },
    error: function (err) {
      alert(err.statusText);
    },
  });
}
// dic.productitems[i].name
// dic.productitems[i].imagefront
// dic.productitems[i].price
// dic.gettotal[i]
// dic.carttotal

function cartpage() {
  $.ajax({
    url: "/cart_page",
    type: "GET",
    // dataType: "json",
    success: function (dic) {
      document.getElementById("cartitems").innerHTML = "";
      for (var i = 0; i < dic.gettotal.length; i++) {
        document.getElementById("cartitems").innerHTML +=
          '<tr>\
                <td class="product-col">\
                    <div class="product">\
                        <figure class="product-media">\
                            <a href="/product/' +
          dic.productitems[i].name +
          '">\
                                <img src="/static' +
          dic.productitems[i].imagefront +
          '" alt="Product image">\
                            </a>\
                        </figure>\
                        <h3 class="product-title">\
                            <a href="/product/' +
          dic.productitems[i].name +
          '">' +
          dic.productitems[i].name +
          '</a>\
                        </h3>\
                    </div>\
                </td>\
                <td class="price-col">' +
          dic.productitems[i].price +
          '</td>\
                <td class="quantity-col">\
                    <div class="cart-product-quantity"> \
                        <a data-product="" id="updatecartremove" onclick="removecart(' +
          dic.productitems[i].id +
          ')" data-action="remove" ><i class="icon-minus"></i></a>\
                        ' +
          dic.orderitems[i].quantity +
          '\
                        <i data-product="" id="updatecartadd" data-action="add" onclick="addcart(' +
          dic.productitems[i].id +
          ')" class="icon-plus"></i>\
                    </div>\
                </td>\
                <td class="total-col">' +
          dic.gettotal[i] +
          '</td>\
                <td class="remove-col"><button class="btn-remove"><i class="icon-close"></i></button></td>\
            </tr>';
      }
      document.getElementById("cartpagetotal").innerHTML =
        '<tr class="summary-subtotal">\
      <td>Subtotal:</td>\
      <td> ' +
        dic.carttotal +
        ' </td>\
  </tr>\
  <tr class="summary-shipping">\
      <td>Shipping:</td>\
      <td>&nbsp;</td>\
  </tr>\
  <tr class="summary-shipping-row">\
      <td>\
          <div class="custom-control custom-radio">\
              <input type="radio" id="free-shipping" name="shipping" class="custom-control-input">\
              <label class="custom-control-label" for="free-shipping">Shipping Fees</label>\
          </div>\
      </td>\
      <td>Rs. 200</td>\
  </tr>\
  <tr class="summary-total">\
      <td>Total:</td>\
      <td>Rs. ' +
        dic.total +
        " </td>\
  </tr>";

      if (dic.carttotal != 0) {
        document.getElementById("cartpagebutton").innerHTML =
          '\
    <a href="/checkout/" class="btn btn-outline-primary-2 btn-order btn-block">\
    PROCEED TO CHECKOUT</a>';
      } else {
        document.getElementById("cartpagebutton").innerHTML =
          '<h5 class="text-center">Cart is Empty</h5>';
      }
    },
    error: function (err) {
      alert(err.statusText);
    },
  });
}

function cartpageoff() {
  $.ajax({
    url: "/cart_page",
    type: "GET",
    // dataType: "json",
    success: function (dic) {
      document.getElementById("cartitemsoff").innerHTML = "";
      document.getElementById("cartitemsoff_tableshead").innerHTML = "";

      document.getElementById("offcanvasheader").innerHTML =
        '<a class="position-relative"><h5\
      class="offcanvas-title" id="offcartlabel">Cart</h5><span \
      class="position-absolute top-0 start-100 translate-middle badge rounded-pill" style="background-color:#D89763;">\
      ' +
        dic.cartitems +
        '</span></a>\
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>';

      if (dic.cartitems == 0) {
        document.getElementById("cartitemsoff").innerHTML +=
          '<div class="text-center align-middle mt-5">\
        <h4>Your Cart is Empty</h4>\
        <a href="/products/" class="btn btn-outline-primary-2 btn-order btn-block">Shop</a>\
    </div>\
        ';
      }

      if (dic.cartitems != 0) {
        document.getElementById("cartitemsoff_tableshead").innerHTML =
          "\
        <tr>\
        <th>Product</th>\
        <th>Quantity</th>\
        <th>Total</th>\
        <th></th>\
        </tr>";

        for (var i = 0; i < dic.gettotal.length; i++) {
          document.getElementById("cartitemsoff").innerHTML +=
            '<tr>\
                <td style="width:400px;" class="product-col">\
                    <div class="product">\
                        <figure class="product-media">\
                            <a href="/product/' +
            dic.productitems[i].name +
            '">\
                                <img src="/static' +
            dic.productitems[i].imagefront +
            '" alt="Product image" width=30>\
                            </a>\
                        </figure>\
                        <h3 class="product-title-off">\
                            <a href="/product/' +
            dic.productitems[i].name +
            '">' +
            dic.productitems[i].name +
            '</a>\
                        </h3>\
                    </div>\
                </td>\
                <td class="quantity-col">\
                    <div class="cart-product-quantity"> \
                        <a data-product="" id="updatecartremove" onclick="removecart(' +
            dic.productitems[i].id +
            ')" data-action="remove" ><i class="icon-minus"></i></a>\
                        ' +
            dic.orderitems[i].quantity +
            '\
                        <i data-product="" id="updatecartadd" data-action="add" onclick="addcart(' +
            dic.productitems[i].id +
            ')" class="icon-plus"></i>\
                    </div>\
                </td>\
                <td class="total-col">' +
            dic.gettotal[i] +
            '</td>\
                <td class="remove-col"><button class="btn-remove"><i class="icon-close"></i></button></td>\
            </tr>';
        }
      }
      document.getElementById("cartpagetotaloff").innerHTML =
        '<tr class="summary-subtotal">\
      <td>Subtotal:</td>\
      <td> ' +
        dic.carttotal +
        " </td>\
      </tr>";

      if (dic.carttotal != 0) {
        document.getElementById("cartpagebuttonoff").innerHTML =
          '\
        <a href="/checkout/" class="btn btn-outline-primary-2 btn-order btn-block">\
        PROCEED TO CHECKOUT</a>';
      } else {
        document.getElementById("cartpagebuttonoff").innerHTML = "";
      }
    },
    error: function (err) {
      alert(err.statusText);
    },
  });
}
