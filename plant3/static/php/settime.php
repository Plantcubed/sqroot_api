<?php
   $date  = $_POST['date'];
   $command = 'sudo date -s ' . $date;
   $output = shell_exec($command);
   echo $output;
?>