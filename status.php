<?php
$logFile = glob(__DIR__ . "/logs/*.log");
rsort($logFile);

if (!$logFile) {
    echo "No builds yet.";
    exit;
}

echo "<pre>";
readfile($logFile[0]);
echo "</pre>";
