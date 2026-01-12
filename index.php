<?php
// Paste your token here
putenv("EXPO_TOKEN=IxQ90f96kL7P5gYL8TnSHD41tyY2W1T1eoR1v065");

// Go to your Expo project folder
chdir("C:\\xampp\\htdocs\\WebAppWrapperExpo");

// Full path to EAS CLI
$easCli = "C:\\Users\\LENOVO\\AppData\\Roaming\\npm\\eas.cmd";

// Run build and capture output
exec("$easCli build --platform android --profile production 2>&1", $output, $returnVar);

// Display logs
echo "<pre>" . implode("\n", $output) . "</pre>";

echo $returnVar === 0 ? "Build completed!" : "Build failed with code $returnVar";
