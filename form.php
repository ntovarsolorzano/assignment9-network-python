<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DHCP Request Form</title>
</head>
<body>
    <h2>DHCP IP Address Request</h2>
    <form action="process.php" method="POST">
        <label for="mac">MAC Address:</label>
        <input type="text" id="mac" name="mac" required pattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$" placeholder="00:1A:2B:3C:4D:5E">
        <br>
        <label for="dhcp_version">DHCP Version:</label>
        <select id="dhcp_version" name="dhcp_version" required>
            <option value="DHCPv4">DHCPv4</option>
            <option value="DHCPv6">DHCPv6</option>
        </select>
        <br>
        <input type="submit" value="Request IP">
    </form>
</body>
</html>
