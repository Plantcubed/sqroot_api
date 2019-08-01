<?php
   $command = 'ifconfig';
   $output = shell_exec($command);
   echo $output;
?>