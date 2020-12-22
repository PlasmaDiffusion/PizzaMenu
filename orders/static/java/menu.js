document.addEventListener("DOMContentLoaded", () => {
  //Drop down buttons
  document.querySelectorAll("button").forEach((button) => {
    if (button.className == "dropdown ui-btn ui-shadow ui-corner-all") {
      //When clicked, this button shows stuff in the table.
      button.onclick = () => {
        var tableBodyChildren =
          button.parentElement.parentElement.parentElement.children;

        //Hide the table
        for (let i = 1; i < tableBodyChildren.length; i++) {
          if (tableBodyChildren[i].style.display == "table-row")
            tableBodyChildren[i].style.display = "none";
          else tableBodyChildren[i].style.display = "table-row";
        }

        //Update topping menus when opened
        if (button.innerHTML == " Toppings ") {
          changeToppingButton(
            document.getElementById("select-native-Toppings")
          );
        } else if (button.innerHTML == " Sub Extras ") {
          changeToppingButton(
            document.getElementById("select-native-Sub Extras")
          );
        }
      };

      //Collapse all menus by default
      var tableBodyChildren =
        button.parentElement.parentElement.parentElement.children;

      for (let i = 1; i < tableBodyChildren.length; i++)
        tableBodyChildren[i].style.display = "none";
    }
  });

  //Have a selector for each pizza you have in your cart. (Changes input form buttons)
  var toppingPizzaSelector = document.getElementById("select-native-Toppings");
  toppingPizzaSelector.onchange = () => {
    changeToppingButton(toppingPizzaSelector);
  };
  var subExtrasSelector = document.getElementById("select-native-Sub Extras");
  subExtrasSelector.onchange = () => {
    changeToppingButton(subExtrasSelector);
  };

  //Show the menu on the left, if there's nothing in the cart. Otherwise it will be on the right. (Desktop view only)
  if (!document.getElementById("cart"))
    document.getElementById("menu").style.float = "left";
});

function changeToppingButton(selector) {
  document.querySelectorAll("form").forEach((form) => {
    if (form.className == "toppingForm") {
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
