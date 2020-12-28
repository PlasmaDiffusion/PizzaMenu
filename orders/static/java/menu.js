document.addEventListener("DOMContentLoaded", () => {
  //Drop down buttons
  document.querySelectorAll("button").forEach((button) => {
    if (button.className == "dropdown ui-btn ui-shadow ui-corner-all") {
      //When clicked, this button shows stuff in the table.
      button.onclick = () => {
        var tableBodyChildren = document.getElementById(button.innerHTML)
          .children;
        //button.parentElement.parentElement.parentElement.children;

        //Hide the table
        for (let i = 1; i < tableBodyChildren.length; i++) {
          if (tableBodyChildren[i].style.display == "table-row")
            tableBodyChildren[i].style.display = "none";
          else tableBodyChildren[i].style.display = "table-row";
        }

        //Update topping menus when opened
        if (button.innerHTML == "Toppings") {
          let toppingElement = document.getElementById(
            "select-native-Toppings"
          );
          toggleDisplay(
            toppingElement.parentElement.parentElement.parentElement
          );
          changeToppingButton(toppingElement);
        } else if (button.innerHTML == "Sub Extras") {
          let subExtrasElement = document.getElementById(
            "select-native-Sub Extras"
          );
          toggleDisplay(
            subExtrasElement.parentElement.parentElement.parentElement
          );
          changeToppingButton(subExtrasElement);
        }
      };

      //Collapse all menus by default
      var tableBodyChildren = document.getElementById(button.innerHTML)
        .children;

      for (let i = 1; i < tableBodyChildren.length; i++)
        tableBodyChildren[i].style.display = "none";
    }
  });

  setupSelectors();

  MoveCartAndMenu();
});

//--------------------------------------------------------------------------------------------------------------------------------
//Global functions
//--------------------------------------------------------------------------------------------------------------------------------

//Show the menu on the left, if there's nothing in the cart. Otherwise it will be on the right. (Desktop view only)
function MoveCartAndMenu() {
  var cartTable = document.getElementById("cartTable");
  if (!cartTable) {
    document.getElementById("menu").style.float = "left";
  } else if (cartTable.children.length > 7) {
    //Center the cart rather than have it be static if there's way too many items
    let cart = document.getElementById("left");
    cart.style.position = "relative";
    cart.style.bottom = "auto";
    document.getElementById("menu").style.float = "none";
  }
}

//Have a selector for each pizza you have in your cart. (Changes input form buttons)
function setupSelectors() {
  var toppingPizzaSelector = document.getElementById("select-native-Toppings");
  toppingPizzaSelector.parentElement.parentElement.parentElement.style.display =
    "none";
  toppingPizzaSelector.onchange = () => {
    changeToppingButton(toppingPizzaSelector);
  };
  var subExtrasSelector = document.getElementById("select-native-Sub Extras");
  subExtrasSelector.parentElement.parentElement.parentElement.style.display =
    "none";
  subExtrasSelector.onchange = () => {
    changeToppingButton(subExtrasSelector);
  };
}

//Hide or show the element using the display style
function toggleDisplay(element) {
  element.style.display = element.style.display == "block" ? "none" : "block";
}

//Change the form buttons based on the selector for the chosen pizza/sub
function changeToppingButton(selector) {
  document.querySelectorAll("form").forEach((form) => {
    if (form.className == "toppingForm" && selector.value) {
      //Show the button/form
      form.style.display = "block";

      //Overwrite the form to have the proper main item id (the last parameter)
      let action = form.action.split("/");
      action[action.length - 2] = selector.value; //Change second last element which would have the argument
      form.action = action.join("/");
      //console.log(form.action);
    }
  });
}
