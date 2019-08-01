<?php
   $command = 'sudo iwlist wlan0 scan | grep ESSID';
   $output = shell_exec($command);
   echo $output;
?>