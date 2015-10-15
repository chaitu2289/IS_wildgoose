<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

class Receiver {

	public function listen() {
		$connection  = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
		$channel = $connection->channel();
		$channel->queue_declare('argus_queue_', false, false, false, false);
		$channel->basic_qos(null, 1, null);
		$channel->basic_consume('argus_queue_', '', false, false, false, false, array($this, 'callback'));
		
		while(count($channel->callbacks)) {
			$channel->wait();
		}
		
		$channel->close();
		$connection->close();
	}
	
	public function callback(AMQPMessage $req) {
		$authResult  = 'chk';
		echo($req->body);
		$msg = new AMQPMessage(json_encode(array('status' => $authResult)), array('correlation_id' => $req->get('correlation_id')));
		$req->delivery_info['channel']->basic_publish($msg, '', $req->get('reply_to'));		
		$req->delivery_info['channel']->basic_ack($req->delivery_info['delivery_tag']);
	}

}


?>
