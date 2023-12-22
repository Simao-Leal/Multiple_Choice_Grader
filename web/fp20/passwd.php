<HTML>
<TITLE>
Fundamentos de programa&ccedil;&atilde;o 2020
</TITLE>
<LINK REL="SHORTCUT ICON" HREF="/~reis.santos/logo.ico">
<BODY BGCOLOR="B5BDD6" link=red vlink=green>
<table border="0" width="100%" cellpadding="5" cellspacing="3">
  <tr align="left" valign="middle"><td>
  <IMG ALIGN=left SRC="istlogo.gif" ALT="IST">
  </td>

  <TD>
  <CENTER>
  <H1>Fundamentos de programa&ccedil;&atilde;o</H1>
  <H2>2020</H2>
  <H3> Departamento de Engenharia Inform&aacute;tica</H3>
  <BR> <BR> <BR> <BR>
<?php
require_once 'CAS.php';
phpCAS::client(CAS_VERSION_3_0,'id.tecnico.ulisboa.pt',443,'/cas');
phpCAS::setCasServerCACert('/etc/ssl/certs/ca-certificates.crt');
phpCAS::handleLogoutRequests(true, array('id.tecnico.ulisboa.pt'));
phpCAS::forceAuthentication();
$user = phpCas::getUser();
$lines = file('passwd.txt');
$found=0;
foreach ($lines as $line) {
	$split = explode(" ", $line);
	if ($user === $split[0]) {
		echo("Password for ".$user."<H1>".$split[1]."</H1><br>\n");
		echo("<H2><A HREF=\"https://web.tecnico.ulisboa.pt/reis.santos/fp20/".$user."\">documentos</A></H2><br>\n");
		$found=1;
	}
}
if ($found == 0) echo("Not found!<br>\n");
?>
</CENTER> </TD> </TABLE> </BODY> </HTML>
