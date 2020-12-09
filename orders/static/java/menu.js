document.addEventListener("DOMContentLoaded", () => {
  //Drop down buttons
  document.querySelectorAll("button").forEach((button) => {
    if (button.className == "dropdown ui-btn ui-shadow ui-corner-all") {
      //When clicked, this button shows stuff in the table.
      button.onclick = () => {
        var tableBodyChildren =
          button.parentElement.parentElement.parentElement.children;

        for (let i = 1; i < tableBodyChildren.length; i++) {
          if (tableBodyChildren[i].style.display == "table-row")
            tableBodyChildren[i].style.display = "none";
          else tableBodyChildren[i].style.display = "table-row";
        }

        /*Change button text
        console.log(button.innerHTML);
        if (button.innerHTML == " &gt; ") button.innerHTML = " v ";
        else button.innerHTML = " &gt; ";*/
      };

      //Collapse all menus by default
      var tableBodyChildren =
        button.parentElement.parentElement.parentElement.children;

      for (let i = 1; i < tableBodyChildren.length; i++)
        tableBodyChildren[i].style.display = "none";
    }
  });
});
