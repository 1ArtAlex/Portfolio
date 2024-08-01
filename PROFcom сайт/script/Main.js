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


//Плавное появление блоков "О нас"
$(document).ready(function () {
    var innerContainer = $(".inner-container");

    $(window).on("scroll", function () {
        var windowHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        var offset = innerContainer.offset().top;

        if (scrollTop + windowHeight > offset) {
            innerContainer.addClass("visible");
        } else {
            innerContainer.removeClass("visible");
        }
    });
});


$(document).ready(function () {
    var aboutLeftContent = $(".first-container");

    $(window).on("scroll", function () {
        var windowHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        var offset = aboutLeftContent.offset().top;

        if (scrollTop + windowHeight > offset) {
            aboutLeftContent.addClass("active");
        } else {
            aboutLeftContent.removeClass("active");
        }
    });
});

$(document).ready(function () {
    var aboutLeftContent = $(".second-container");

    $(window).on("scroll", function () {
        var windowHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        var offset = aboutLeftContent.offset().top;

        if (scrollTop + windowHeight > offset) {
            aboutLeftContent.addClass("active");
        } else {
            aboutLeftContent.removeClass("active");
        }
    });
});


//обратный отсчет в статистике
document.addEventListener("DOMContentLoaded", function () {
    const numberBlocks = document.querySelectorAll(".number-block");

    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScroll() {
        numberBlocks.forEach((block) => {
            if (!block.hasAttribute("data-animated") && isElementInViewport(block)) {
                block.setAttribute("data-animated", "true");

                const targetCount = parseFloat(block.getAttribute("data-count"));
                let currentCount = 0;

                const updateCount = () => {
                    if (currentCount < targetCount) {
                        const remainingDifference = targetCount - currentCount;
                        const step = remainingDifference / 50; // Изменил здесь для более равномерной анимации

                        currentCount = currentCount + step > targetCount ? targetCount : currentCount + step;

                        const formattedCount = block.classList.contains('decimal') ? currentCount.toFixed(1) + "%" : Math.round(currentCount);

                        block.querySelector(".count").textContent = formattedCount;
                        requestAnimationFrame(updateCount);
                    }
                };

                updateCount();
            }
        });
    }

    // Вызываем handleScroll при прокрутке страницы
    window.addEventListener("scroll", handleScroll);

    // Вызываем handleScroll при загрузке страницы для проверки видимости блоков
    handleScroll();
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
