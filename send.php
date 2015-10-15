<?php
/*
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
$channel->queue_declare('rpc_queue', false, false, false, false);



$callback = function($msg) {
  echo " [x] Received ", $msg->body, "\n";
};
$channel->queue_declare('hello', false, false, false, false);
$msg = new AMQPMessage('Hello World!');
$channel->basic_publish($msg, '', 'hello');
echo " [x] Sent 'Hello World!'\n";
$channel->basic_consume('hello', '', false, true, false, false, $callback);
while(count($channel->callbacks)) {
    echo 'chaitanya';
    $channel->wait();
}
$channel->close();
$connection->close();
*/


require_once('sender.php');

$simple_sender = new Sender();
echo($simple_sender->execute('chaitanya'));




?>
