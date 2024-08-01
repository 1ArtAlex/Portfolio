<?php
    $name = $_POST['name'];
    $website = $_POST['website'];
	$phone = $_POST['phone'];
    $email = $_POST['email'];
    $text = $_POST['text'];

	$to = "alex.art.0205@mail.com";
	$date = date ("d.m.Y");
	$time = date ("h:i");
	$from = $email;
	$subject = "Заявка c сайта";


	$msg="
    Имя: $name /n
    Сайт: $website /n
    Телефон: $phone /n
    Почта: $email /n
    Текст: $text";
	mail($to, $subject, $msg, "From: $from ");

?>

