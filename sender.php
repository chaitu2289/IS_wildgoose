<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

class Sender {
	
	private $response;
	private $corr_id;

	

	public function execute($message) {
		$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
		$channel = $connection->channel();
		list($callback_queue, ,) = $channel->queue_declare('', false, false, true, false);
		$channel->basic_consume($callback_queue, '', false, false, false, false, array($this, 'onResponse'));
		$this->response = null;
		$this->corr_id = uniqid();
		
		$msg = new AMQPMessage($message, array('correlation_id' => $this->corr_id, 'reply_to' => $callback_queue));
		$channel->basic_publish($msg, '', 'argus_queue_');
		
		while (!$this->response) {
			$channel->wait();
		}
		$channel->close();
		$connection->close();
		
		return $this->response;
	}
	
	public function onResponse(AMQPMessage $rep) {
		if($rep->get('correlation_id') == $this->corr_id) {
			$this->response = $rep->body;
		}	
	}

}

?>
