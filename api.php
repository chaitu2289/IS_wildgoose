<?php

require_once('sender.php');

//$mongo = new MongoClient();
//$db = $mongo->it;
//$images = $db->images;
//$labels = $db->labels;
//$page = $pages->findOne(array('_id' => $_REQUEST['_id']));

if (!isset($_REQUEST['op'])) {
	echo json_encode(array("status" => "error", "description" => "op not specified"));
	exit;
}

$callback = function($msg) {
	var_dump($msg->body);
};

error_log("received request with OP $_REQUEST[op]");

switch($_REQUEST['op']) {
case 'identify_objects':
	$image = $_FILES['test_image']['tmp_name'];
	$simple_sender = new Sender();
	//$resp = $simple_sender->execute($image);
	//var_dump(json_encode($resp));
	//echo " [x] Image sent\n";	
	$label1 = array('_id' => 1, 'box' => array(array(0,0), array(150,150)), 'tag' => 'chair');
	$label2 = array('_id' => 2, 'box' => array(array(50,50), array(50,50)), 'tag' => 'car');

	$resp = array('_id' => 1, 'labels' => array($label1, $label2) );

	break;
case 'learn_features':
	break;
default:
	echo json_encode(array("status" => "error", "description" => "unknown op '$_REQUEST[op]'"));
	exit;
}

//$resp = array("_id" => 1, "labels" => array(array("_id" => 2, box => array(array(1,2),array(3,4)))));

echo json_encode($resp);
