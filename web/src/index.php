<HTML> <TITLE> COMPILADORES 2020 </TITLE>
<BODY BGCOLOR="B5BDD6" link=red vlink=green>
<table border="0" width="100%" cellpadding="5" cellspacing="3">
  <tr align="left" valign="middle"><td>
  <IMG ALIGN=left SRC="istlogo.gif" ALT="IST">
  </td>

  <TD>
  <CENTER> <H1>COMPILADORES (taguspark)</H1> <H2>2020</H2>
  <H3> Departamento de Engenharia Inform&aacute;tica</H3>
  <H3> Pedro Reis dos Santos</H3>
  <BR> <BR> <BR> <BR>
  </TD>
</TABLE>
<HR size=2 noshade> <BR>
<?php
require_once 'CAS.php';
phpCAS::client(CAS_VERSION_3_0,'id.tecnico.ulisboa.pt',443,'/cas');
phpCAS::setCasServerCACert('/etc/ssl/certs/AddTrust_External_Root.pem');
phpCAS::handleLogoutRequests(true, array('id.tecnico.ulisboa.pt'));
phpCAS::forceAuthentication();
?>

<?php
$user = phpCas::getUser();
// $user = "ist177995";

// decode file
$name = "co20pw.bcca";
$fp = fopen($name, "rb");
$file = fread($fp, filesize($name));
fclose($fp);
$x = 200;
$p = "";
for ($i = 0; $i < strlen($file); $i++) {
	$p .= chr($x - ord($file[$i]));
	$x = ord($file[$i]);
}

// search for passwd
$found=0;
$lines = explode("\n", $p);
foreach ($lines as $line) {
	$split = explode(" ", $line);
	if ($user === $split[0]) {
		echo("<A HREF=\"" . $user . "\">https://web.tecnico.ulisboa.pt/~reis.santos/co20/" . $user . "</A><br>\n");
		echo("<H2>Username: ".$user."</H2>\n");
		echo("<H2>Password: ".$split[1]."</H2>\n");
		$found=1;
	}
}
if ($found == 0) echo("<h1>User: ".$user. ", not found!</h1>\n");
?>
</BODY></HTML>
