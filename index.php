<?php
// Set token for non-interactive authentication
putenv("EXPO_TOKEN=IxQ90f96kL7P5gYL8TnSHD41tyY2W1T1eoR1v065");

// Change to project directory
chdir("C:\\xampp\\htdocs\\WebAppWrapperExpo");

// Full path to eas CLI
$easCli = "C:\\Users\\LENOVO\\AppData\\Roaming\\npm\\eas.cmd";

// Run build, capture stdout and stderr
exec("$easCli build --platform android --profile production 2>&1", $output, $returnVar);

// Display output
echo "<pre>" . implode("\n", $output) . "</pre>";
echo $returnVar === 0 ? "Build completed!" : "Build failed with code $returnVar";
