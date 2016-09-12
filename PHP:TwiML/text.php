<?php

echo '<?xml version="1.0" encoding="UTF-8" ?>\n';


if(isset($_REQUEST['MessageStatus'])) {
	if ($_REQUEST['MessageStatus'] == 'failed')
	{ 
	$log = fopen("error_log.php", "a");
	
	error_message = "The following message failed to send. MessageSid: ".$_REQUEST['MessageSid']."\n AccountSid: ".$_REQUEST['AccountSid']."\n From: ".$_REQUEST['From']."\n To: ".$_REQUEST['To']."\n Body: ".$_REQUEST['Body'] ;

	fwrite($log, error_message);
	fclose($log);
	exit ("message failed to send"); 
	}
	else {
	exit("message successfully sent");
	}
}

$flag = 0;
$body = $_REQUEST['Body'];   
 
$body = explode ("", $body);
for($i = 0; $i < count($body); $i++) {
	if($body[$i] == "1" || $body[$i] == "2" || $body[$i] == "3") { 
		$body = $body[$i];
		$flag = 1;
		break;
	}
}

#ask again if input incorrect
if ($flag != 1) { 
echo '<Response><Message statusCallback="/twilio-responder.php">';
echo 'Please respond with 1, 2, or 3.';
echo '</Message></Response>';

}

#format is +1112223333 
$from = $_REQUEST['From'];


if ($body == "1") {
echo '<Response><Message statusCallback="/confirm.php">';
echo 'We have confirmed your appointment. If you would like to undo this action, reply 1.';
echo '</Message></Response>';

}

else if ($body == "2") {
echo '<Response><Message statusCallback="/cancel.php">';
echo 'We have cancelled your appointment. If you would like to undo this action, reply 1.';
echo '</Message></Response>';

}

else if ($body == "3") {
echo '<Response><Message statusCallback="/reschedule.php">';
echo 'If you would like to reschedule your appointment right now, reply 1.  If you would like to speak to your service provider, reply 2.';
echo '</Message></Response>';

}


?>