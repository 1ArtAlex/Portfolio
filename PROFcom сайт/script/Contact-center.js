//Все что связано в бургер меню
document.getElementById('burger').addEventListener('click', function () {
    const menu = document.getElementById('menu');
    const closeButton = menu.querySelector('.close-button');

    if (menu.style.right === '-250px' || menu.style.right === '') {
        menu.style.right = '0';
        closeButton.style.display = 'block';
    } else {
        menu.style.right = '-250px';
        closeButton.style.display = 'none';
    }
});

document.querySelector('.close-button').addEventListener('click', function () {
    const menu = document.getElementById('menu');
    const closeButton = menu.querySelector('.close-button');

    menu.style.right = '-250px';
    closeButton.style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
    const burgerMenu = document.getElementById('menu');
    const burgerButton = document.getElementById('burger');

    burgerButton.addEventListener('click', function (event) {
        burgerMenu.classList.toggle('active');
        event.stopPropagation();
    });

    const closeBtn = document.querySelector('.close-button');

    closeBtn.addEventListener('click', function () {
        burgerMenu.classList.remove('active');
    });

    document.addEventListener('click', function (event) {
        const burgerMenu = document.getElementById('menu');
        const burgerButton = document.getElementById('burger');
        const isClickInsideBurgerMenu = burgerMenu.contains(event.target) || burgerButton.contains(event.target);
        const isBurgerMenuActive = burgerMenu.classList.contains('active');

        if (!isClickInsideBurgerMenu && isBurgerMenuActive) {
            burgerMenu.classList.remove('active');
            burgerMenu.style.right = '-250px';
            const closeButton = burgerMenu.querySelector('.close-button');
            closeButton.style.display = 'none';
        }
    });

});

document.getElementById('burger').addEventListener('focus', function () {
    document.getElementById('menu').classList.add('hide-button');
});

document.getElementById('burger').addEventListener('blur', function () {
    document.getElementById('menu').classList.remove('hide-button');
});


//Модальные окна
document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("myBtn");
    var footerBtn = document.getElementById("want-widget-footer");
    var span = document.getElementsByClassName("close")[0];

    function closeModal(modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    function openModal(modal) {
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    btn.onclick = function () {
        openModal(modal);
    }

    footerBtn.onclick = function () {
        openModal(modal);
    }

    span.onclick = function () {
        closeModal(modal);
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal(modal);
        }
    }

    // Добавленные функции

    function openModal(modal) {
        modal.style.display = "block";
        document.documentElement.style.overflow = "hidden";
    }

    function closeModal(modal) {
        modal.style.display = "none";
        document.documentElement.style.overflow = "auto";
    }
});



// Ввод номера телефона
function setCursorPosition(pos, e) {
    e.focus();
    if (e.setSelectionRange) e.setSelectionRange(pos, pos);
    else if (e.createTextRange) {
        var range = e.createTextRange();
        range.collapse(true);
        range.moveEnd("character", pos);
        range.moveStart("character", pos);
        range.select();
    }
}

function mask(e) {
    var matrix = "+7 (___) ___-__-__",
        i = 0,
        def = matrix.replace(/\D/g, ""),
        val = this.value.replace(/\D/g, "");
    def.length >= val.length && (val = def);
    matrix = matrix.replace(/[_\d]/g, function (a) {
        return val.charAt(i++) || "_";
    });
    this.value = matrix;
    i = matrix.lastIndexOf(val.substr(-1));
    i < matrix.length && matrix != "+7 (___) ___-__-__" ? i++ : i = matrix.indexOf("_");
    setCursorPosition(i, this);
}

document.addEventListener("DOMContentLoaded", function () {
    var input = document.querySelector("#online_phone");
    input.addEventListener("input", mask, false);
    input.addEventListener("click", function () {
        var pos = input.value.indexOf("_");
        setCursorPosition(pos !== -1 ? pos : input.value.length, input);
    });
    input.focus();
    setCursorPosition(0, input);
});

//анимация текст в модальном окне
document.getElementById('text').addEventListener('focus', function() {
    var label = document.getElementById('text-label');
    label.style.top = '-11px';
    label.classList.add('active'); /* Добавление класса при поднятии */
});

document.getElementById('text').addEventListener('blur', function() {
    var label = document.getElementById('text-label');
    if (this.value == '') {
        label.style.top = '15px';
        label.classList.remove('active'); /* Удаление класса при спуске */
    }
});



//Планое появление
$(document).ready(function () {
    var burgersitems = $(".burgers-items");

    $(window).on("scroll", function () {
        var windowHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        var offset = burgersitems.offset().top;

        if (scrollTop + windowHeight > offset) {
            burgersitems.addClass("active");
        } else {
            burgersitems.removeClass("active");
        }
    });
});


//Стрелочки на возможностях контакт центра
function initializeTextBlocks() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach((menuItem) => {
        const textContainer = menuItem.querySelector('.text-container');
        const textBlocks = textContainer.querySelectorAll('.text-block');
        let currentTextIndex = 1;
        const prevButton = menuItem.querySelector('.prev-btn');
        prevButton.addEventListener('click', () => {
            currentTextIndex = (currentTextIndex === 1) ? textBlocks.length : currentTextIndex - 1;
            updateTextBlocksPosition(textBlocks, currentTextIndex);
        });
        const nextButton = menuItem.querySelector('.next-btn');
        nextButton.addEventListener('click', () => {
            currentTextIndex = (currentTextIndex === textBlocks.length) ? 1 : currentTextIndex + 1;
            updateTextBlocksPosition(textBlocks, currentTextIndex);
        });
        updateTextBlocksPosition(textBlocks, currentTextIndex);
    });
}
function updateTextBlocksPosition(textBlocks, index) {
    textBlocks.forEach((block, blockIndex) => {
        block.style.transform = `translateX(${100 * (blockIndex + 1 - index)}%)`;
    });
}
document.addEventListener('DOMContentLoaded', initializeTextBlocks);



//Кнопка ↑
document.addEventListener("DOMContentLoaded", function () {
    var scrollToTopBtn = document.getElementById("scrollToTopBtn");
    window.addEventListener("scroll", function () {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 600) {
            scrollToTopBtn.style.display = "block";
        } else {
            scrollToTopBtn.style.display = "none";
        }
    });
    scrollToTopBtn.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});


//Автоматическое обновление года
document.addEventListener("DOMContentLoaded", function () {
    var currentYear = new Date().getFullYear();
    document.getElementById("copyright").innerHTML = "Copyright PROFcom © " + currentYear + ". All rights reserved.";
});
