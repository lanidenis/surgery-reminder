<?php

$server = mysql_connect("localhost", 'jdenis', 'jdenis');
if (! $server ) { 
	die('Could not connect to server');
}

$result = mysql_select_db('patient_db', $server);
if (! $result) {
	die('Could not select database');
}

$sql = "select * from patient_records WHERE (MRN == 0";
$retval = mysql_query($sql, $server)

digits = explode("", $_REQUEST['Digits']);
digits = implode(" ", digits);

<-- left off here-->

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<Response><Gather action=\"process_gather2.php\" method=\"GET\">";
echo "<Say>You entered " . digits . ". Is this correct? Press 1 for yes, or 2 for no.</Say></Gather></Response>";

mysql_close($server);
?>