<?php
header('Content-Type: text/html');
{
  $ptf = $_POST['Ptf'];
  $brw = $_POST['Brw'];
  $cc = $_POST['Cc'];
  $ram = $_POST['Ram'];
  $ht = $_POST['Ht'];
  $wd = $_POST['Wd'];
  $os = $_POST['Os'];

  function getIP() {
    if (isset($_SERVER["HTTP_CF_CONNECTING_IP"])) {
        $_SERVER['REMOTE_ADDR'] = $_SERVER["HTTP_CF_CONNECTING_IP"];
        $_SERVER['HTTP_CLIENT_IP'] = $_SERVER["HTTP_CF_CONNECTING_IP"];
    }

    $client  = @$_SERVER['HTTP_CLIENT_IP'];
    $forward = @$_SERVER['HTTP_X_FORWARDED_FOR'];
    $remote  = $_SERVER['REMOTE_ADDR'];

    if(filter_var($client, FILTER_VALIDATE_IP))
    {
        $ipdetails = $client;
    }
    elseif(filter_var($forward, FILTER_VALIDATE_IP))
    {
        $ipdetails = $forward;
    }
    else
    {
        $ipdetails = $remote;
    }
    return $ipdetails;
  }

  $ipdetails = getIP();
  $data = array('platform' => $ptf,
  'browser' => $brw,
  'cores' => $cc,
  'ram' => $ram,
  'ip' => $ipdetails,
  'ht' => $ht,
  'wd' => $wd,
  'os' => $os);

  $json_data = json_encode($data);

  $f = fopen("../../logs/data.txt", 'w+');
  fwrite($f, $json_data);
  fclose($f);
}