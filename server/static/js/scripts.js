
window.addEventListener('DOMContentLoaded', event => {

const title = document.getElementById("greeting");
const text = title.innerHTML;
title.innerHTML = ""
let index = 0;

function type() {
    title.innerHTML += text[index];
    index++;
    if (index < text.length) {
    setTimeout(type, 50);
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
const cityInput = document.getElementById("cityInput");

imageSelectButton.addEventListener("click", () => {
  const input = document.createElement("input");
  input.type = "file";


  
  input.addEventListener("change", (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    const formData = new FormData();
    formData.append("image", file);
    console.log(cityInput.value)
    formData.append("message", cityInput.value);

    const options = {
        method: 'POST',
        body: formData,
        mode: 'no-cors'
    };
    fetch( 'http://192.168.2.39:5002/fit', options )
        .then( function(response) { return response.json() } )
        .catch(error => {console.error(error)})
        .then( function(data) {
            console.log(data.image);
            console.log(data.message);
            display_fit(data.message);
            selectedImage.src = 'data:image/jpeg;base64,' + data.image;
          })

    reader.onload = (event) => {
      selectedImage.src = event.target.result;
    };
    reader.readAsDataURL(file);
  });

  input.click();
});


const fitDescription = document.getElementById("description");
let indexDisplay = 0;
description.innerHTML= "";

const head = document.getElementById("head");
const headBobRate = 4;
var headBobAmt = 0.1;

function display_fit(x) {
    if (indexDisplay == 0) {
        description.innerHTML = ""
    }
    if (indexDisplay % headBobRate == 0) {
        headBobAmt *= -1
        head.style.transform = 'rotate(' + headBobAmt + 'rad)';
    }
    if (x[indexDisplay] == "X") {
        description.innerHTML += '\n';
    } else {
        description.innerHTML += x[indexDisplay];
    }
    indexDisplay++;
    if (indexDisplay < x.length) {
        setTimeout(display_fit, 5, x);
    } else {
        indexDisplay = 0;
        animateBowtie()
        head.style.transform = 'rotate(0rad)';
    }
}

const bowtie = document.getElementById("bowtie");
const bowtieLimits = 0.2
let bowtieRotSpeed = 0.02;
let rot = 0;

function animateBowtie() {
    if (indexDisplay != 0) {
        rot = 0;
        bowtie.style.transform = 'rotate(' + rot + 'rad)';
    } else {
        rot += bowtieRotSpeed
        if (rot > bowtieLimits || rot < -bowtieLimits) {
            bowtieRotSpeed *= -1;
        }
        bowtie.style.transform = 'rotate(' + rot + 'rad)';
        requestAnimationFrame(animateBowtie);
    }
}

animateBowtie()