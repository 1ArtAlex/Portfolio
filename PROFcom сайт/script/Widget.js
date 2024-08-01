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
    function openModal(modal) {
        modal.style.display = "block";
        document.documentElement.style.overflow = "hidden";
    }

    function closeModal(modal) {
        modal.style.display = "none";
        document.documentElement.style.overflow = "auto";
    }

    function setupModal(btn, modal, span, btnLeaveCallback) {
        btn.onclick = function () {
            openModal(modal);
        }

        span.onclick = function () {
            closeModal(modal);
        }

        if (btnLeaveCallback) {
            btnLeaveCallback.onclick = function () {
                closeModal(modal);
                openModal(modalMain); // Замените modalMain на идентификатор вашего основного модального окна
            }
        }
    }

    var modalMain = document.getElementById("myModal");
    var btnMain = document.getElementById("myBtn");
    var spanMain = document.getElementsByClassName("close")[0];

    setupModal(btnMain, modalMain, spanMain);

    var modalCallback = document.getElementById("modal-callback");
    var btnCallback = document.getElementById("btn-callback");
    var spanCallback = document.getElementsByClassName("close-callback")[0];
    var btnLeaveCallbackCallback = document.getElementById("want-callback");

    setupModal(btnCallback, modalCallback, spanCallback, btnLeaveCallbackCallback);

    var modalGenerator = document.getElementById("modal-generator");
    var btnGenerator = document.getElementById("btn-generator");
    var spanGenerator = document.getElementsByClassName("close-generator")[0];
    var btnLeaveCallbackGenerator = document.getElementById("want-generator");

    setupModal(btnGenerator, modalGenerator, spanGenerator, btnLeaveCallbackGenerator);

    var modalOnlineChat = document.getElementById("modal-onlinechat");
    var btnOnlineChat = document.getElementById("btn-onlinechat");
    var spanOnlineChat = document.getElementsByClassName("close-onlinechat")[0];
    var btnLeaveCallbackOnlineChat = document.getElementById("want-onlinechat");

    setupModal(btnOnlineChat, modalOnlineChat, spanOnlineChat, btnLeaveCallbackOnlineChat);

    var modalQuiz = document.getElementById("modal-quiz");
    var btnQuiz = document.getElementById("btn-quiz");
    var spanQuiz = document.getElementsByClassName("close-quiz")[0];
    var btnLeaveCallbackQuiz = document.getElementById("want-quiz");

    setupModal(btnQuiz, modalQuiz, spanQuiz, btnLeaveCallbackQuiz);

    var modalInstinct = document.getElementById("modal-instinct");
    var btnInstinct = document.getElementById("btn-instinct");
    var spanInstinct = document.getElementsByClassName("close-instinct")[0];
    var btnLeaveCallbackInstinct = document.getElementById("want-instinct");

    setupModal(btnInstinct, modalInstinct, spanInstinct, btnLeaveCallbackInstinct);

    var modalMultibutton = document.getElementById("modal-multibutton");
    var btnMultibutton = document.getElementById("btn-multibutton");
    var spanMultibutton = document.getElementsByClassName("close-multibutton")[0];
    var btnLeaveCallbackMultibutton = document.getElementById("want-multibutton");

    setupModal(btnMultibutton, modalMultibutton, spanMultibutton, btnLeaveCallbackMultibutton);

    var rightMyBtn = document.getElementById("right-myBtn");
    rightMyBtn.onclick = function () {
        openModal(modalMain);
    }

    var footerBtn = document.getElementById("want-widget-footer");
    footerBtn.onclick = function () {
        openModal(modalMain);
    }

    // Обработка кликов по окну для закрытия
    window.onclick = function (event) {
        if (event.target == modalMain) {
            closeModal(modalMain);
        } else if (event.target == modalCallback) {
            closeModal(modalCallback);
        } else if (event.target == modalGenerator) {
            closeModal(modalGenerator);
        } else if (event.target == modalOnlineChat) {
            closeModal(modalOnlineChat);
        } else if (event.target == modalQuiz) {
            closeModal(modalQuiz);
        } else if (event.target == modalInstinct) {
            closeModal(modalInstinct);
        } else if (event.target == modalMultibutton) {
            closeModal(modalMultibutton);
        }
        // Добавьте аналогичные блоки кода для других модальных окон...
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


//Увеличение экрана card
document.addEventListener("DOMContentLoaded", function () {
    var cards = document.querySelectorAll('.card');

    function isElementInViewport(element) {
        var rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScroll() {
        cards.forEach(function (card) {
            if (isElementInViewport(card)) {
                card.classList.add('visible');
            } else {
                card.classList.remove('visible');
            }
        });
    }

    window.addEventListener('scroll', handleScroll);
});


document.addEventListener("DOMContentLoaded", function() {
    var navItemWidgets = document.querySelectorAll('.nav-item-widget');

    navItemWidgets.forEach(function(widget) {
        widget.addEventListener('click', function() {
            var description = this.querySelector('.description');
            if (description.style.display === 'block') {
                description.style.display = 'none';
            } else {
                description.style.display = 'block';
            }
        });
    });
});


//Анимация картинок при наведении на шаги
document.addEventListener("DOMContentLoaded", function () {
    var navItems = document.querySelectorAll('.nav-item-widget');
    var images = document.querySelectorAll('.history-images img');

    navItems.forEach(function (navItem, index) {
        navItem.addEventListener('mouseover', function () {
            resetImages(); // Сброс всех картинок в исходное положение
            images[index].classList.add('active');
        });

        navItem.addEventListener('mouseout', function () {
            images[index].classList.remove('active');
        });
    });

    function resetImages() {
        images.forEach(function (image) {
            image.classList.remove('active');
        });
    }
});


// Добавить обработчик события для плюса и крестика у шагов
document.querySelectorAll('.plus, .cross').forEach(element => {
    element.addEventListener('click', function () {
    });
});


//Отзывы
$(document).ready(function () {
    // Инициализация Slick Slider
    $('.karusetulava').slick({
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        responsive: [{
            breakpoint: 850,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
                infinite: true,
            }
        }]
    });

    // Обработчики событий для стрелочек
    $('.prev-slide').on('click', function () {
        $('.karusetulava').slick('slickPrev');
    });

    $('.next-slide').on('click', function () {
        $('.karusetulava').slick('slickNext');
    });
});



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
