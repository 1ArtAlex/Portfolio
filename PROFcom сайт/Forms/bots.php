<?php
    $name = $_POST['name'];
	$phone = $_POST['phone'];
    $text = $_POST['text'];

	$to = "alex.art.0205@mail.com";
	$date = date ("d.m.Y");
	$time = date ("h:i");
	$from = $email;
	$subject = "Заявка c сайта";


	$msg="
    Имя: $name /n
    Телефон: $phone /n
    Текст: $text";
	mail($to, $subject, $msg, "From: $from ");

?>

