
window.addEventListener('DOMContentLoaded', event => {

const title = document.getElementById("greeting");
const text = title.innerHTML;
title.innerHTML = ""
let index = 0;

function type() {
    title.innerHTML += text[index];
    index++;
    if (index < text.length) {
    setTimeout(type, 150);
    } else {
        type1()  }
}
type();

const title1 = document.getElementById("greeting1");
const text1 = title1.innerHTML;
title1.innerHTML = ""
let index1 = 0;

function type1(){
    title1.innerHTML += text1[index1];
    index1++;
    if (index1 < text1.length) {
    setTimeout(type1, 100);
    }

}

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 72,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

const imageSelectButton = document.getElementById("image-select-button");
const selectedImage = document.getElementById("selected-image");

imageSelectButton.addEventListener("click", () => {
  const input = document.createElement("input");
  input.type = "file";

  input.addEventListener("change", (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      selectedImage.src = event.target.result;
      selectedImage.style.display = "block";
    };
    reader.readAsDataURL(file);
  });

  input.click();
});

