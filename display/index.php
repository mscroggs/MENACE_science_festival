<!-- 1920x1080 -->

<html>
<head>
<title>MENACE</title>
<style type='text/css'>
table.invisible,
table.invisible tr,
table.invisible td {border:0}
table.totals,
table.totals tr,
table.totals td {border:0}
table.totals td {width:100px;text-align:center;font-size:30px;padding-top:30px;padding-bottom:30px}
table.totals span {font-size:60px}
table {margin-left:auto;margin-right:auto}
body {text-align:center;font-family:"Latin Modern Mono",serif}
</style>
</head>
<body>
<div style='text-align:center;padding-right:100px'>
<?php
if(file_exists('_files/logo.png')){
echo("
<img src='_files/logo.png' id='logob' style='width:200px;margin-top:30px'><br />");
if(file_exists('_files/logo-overlay.png')){
echo("
<img src='_files/logo-overlay.png' style='width:200px;margin-top:-126px'>
<br />");}}
?>
<img src='line.png' id='linePlot' style='width:1200px;'>
</div>
<div style='position:absolute;right:120px;top:120px'>
<table class='totals' style='margin-top:50px'>
<tr>
<td>MENACE wins<br /><span id='won'>0</span></td>
</tr><tr>
<td>draws<br /><span id='drawn'>0</span></td>
</tr><tr>
<td>human wins<br /><span id='lost'>0</span></td>
</tr>
</table>
</div>
<div style='text-align:center;font-size:20px;position:absolute;top:45px;right:45px;width:250px'>Follow my learning progress on Twitter: <span style='padding-right:4px;font-size:35px;color:#4da8f3;font-family:"Chalkdust Icon Font"'>a</span>@MENACElearns</div>
<div style='text-align:center;font-size:20px;position:absolute;bottom:12px;right:45px;width:250px'>#ItsAllAcademic</div>
<script type='text/javascript'>
<?php
if(file_exists('_files/logo-blinkfast-small.gif')){
echo("
function blink(){
    document.getElementById('logob').src='_files/logo-blinkfast-small.gif'
    setTimeout(blink, 1000*(3+Math.random()*10));
}

blink()

");}
?>

function reloadIMG(){
    document.getElementById('linePlot').src='line.png?t=' + new Date().getTime()
}

setInterval(reloadIMG, 2000);

var loader;
loader = new XMLHttpRequest();
loader.onreadystatechange=function(){
    if(loader.readyState==4 && loader.status==200){
        ns = loader.responseText.split(",");
        document.getElementById("won").innerHTML=ns[0];
        document.getElementById("drawn").innerHTML=ns[1];
        document.getElementById("lost").innerHTML=ns[2];
        setTimeout(reloadN, 2000);
    }
}

function reloadN(){
    loader.open("GET","numbers.txt?t=" + new Date().getTime());
    loader.send();
}
reloadN()
</script>
</body>
</html>
