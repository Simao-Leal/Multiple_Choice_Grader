<HTML>
<TITLE>
COMPILADORES 2020
</TITLE>
<BODY BGCOLOR="B5BDD6" link=red vlink=green>
<table border="0" width="100%" cellpadding="5" cellspacing="3">
  <tr align="left" valign="middle"><td>
  <IMG ALIGN=left SRC="istlogo.gif" ALT="IST">
  </td>

  <TD>
  <CENTER>
  <H1>COMPILADORES</H1>
  <H2>2020</H2>
  <H3> Departamento de Engenharia Inform&aacute;tica</H3>
  <BR> <BR> <BR> <BR>
  </TD>
</TABLE>
<HR size=2 noshade> <BR>
<?php
// Import server's phpCAS library.
require_once 'CAS.php';
// Initialize phpCAS
phpCAS::client(CAS_VERSION_3_0,'id.tecnico.ulisboa.pt',443,'/cas');
// Set CAS server certificate
phpCAS::setCasServerCACert('/etc/ssl/certs/AddTrust_External_Root.pem');
// Set logout handler
phpCAS::handleLogoutRequests(true, array('id.tecnico.ulisboa.pt'));
// Force CAS authentication
phpCAS::forceAuthentication();
// If the code reaches this step, the user has already been authenticated by the CAS server
// and the user's IST ID can be read with phpCAS::getUser().
?>

<?php
$user = phpCas::getUser();
// If all is right the next line will print the users IST ID.
echo("Hello " . $user . "!<br>\n");
$lines = file('file.txt');
$found=0;
foreach ($lines as $line) {
	$split = explode(" ", $line);
	if ($user === $split[0]) {
		echo("Found: ".$split[1]."<br>\n");
		$found=1;
	}
}
if ($found == 0) echo("Not found!<br>\n");
?>
</BODY></HTML>
