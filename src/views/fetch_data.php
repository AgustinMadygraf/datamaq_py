<?php
/* 
Migrar `fetch_data.php` hacia Flask
*/

require "database_connection.php";

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

$sql = "SELECT * FROM registros_modbus WHERE `valor` IS NOT NULL";
$result = $conn->query($sql);
$datos = array();

while($row = $result->fetch_assoc()) {
    $datos[] = $row;
}

echo json_encode($datos);

$conn->close();
