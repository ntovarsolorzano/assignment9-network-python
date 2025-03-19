<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac = escapeshellarg($_POST["mac"]);
    $dhcp_version = escapeshellarg($_POST["dhcp_version"]);

    // Execute Python script and capture output
    $command = "python3 network_config.py $mac $dhcp_version";
    $output = shell_exec($command);
    
    // Decode JSON response
    $response = json_decode($output, true);

    if (isset($response["error"])) {
        echo "<h3>Error: " . htmlspecialchars($response["error"]) . "</h3>";
    } else {
        echo "<h3>Assigned IP</h3>";
        echo "<p>MAC Address: " . htmlspecialchars($response["mac_address"]) . "</p>";
        echo "<p>Assigned IP: " . htmlspecialchars($response["assigned_ip"]) . "</p>";
        echo "<p>Lease Time: " . htmlspecialchars($response["lease_time"]) . "</p>";
        echo "<p>Subnet: " . htmlspecialchars($response["subnet"]) . "</p>";
    }
} else {
    echo "<h3>Invalid Request</h3>";
}
?>
