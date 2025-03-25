-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 25-03-2025 a las 19:29:50
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `novus`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_modbus`
--

CREATE TABLE `registros_modbus` (
  `ID` int(11) NOT NULL,
  `direccion_modbus` int(11) NOT NULL,
  `registro` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `rw` varchar(5) DEFAULT NULL,
  `acceso` varchar(20) DEFAULT NULL,
  `valor` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `registros_modbus`
--

INSERT INTO `registros_modbus` (`ID`, `direccion_modbus`, `registro`, `descripcion`, `rw`, `acceso`, `valor`) VALUES
(1, 0, 'HR_NUM_SERIE_LO', 'Número de serie del dispositivo (1/2 registros)', 'R', '16 bits', NULL),
(2, 1, 'HR_NUM_SERIE_HI', 'Número de serie del dispositivo (2/2 registros)', 'R', '16 bits', NULL),
(3, 2, 'HR_HW_SET_LO ', 'Configuración del hardware presente. (1/2 registros)', 'R', '16 bits', NULL),
(4, 3, 'HR_HW_SET_HI ', 'Configuración del hardware presente. (2/2 registros)', 'R', '16 bits', NULL),
(5, 4, 'HR_ETH_MAC0  ', 'Dirección MAC de la interfaz Ethernet: 6H:6L:5H:5L:4H:4L', 'R', '16 bits', NULL),
(6, 5, 'HR_ETH_MAC1  ', 'Dirección MAC de la interfaz Ethernet: 6H:6L:5H:5L:4H:4L', 'R', '16 bits', NULL),
(7, 6, 'HR_ETH_MAC2  ', 'Dirección MAC de la interfaz Ethernet: 6H:6L:5H:5L:4H:4L', 'R', '16 bits', NULL),
(8, 7, 'HR_TS_CALIB0 ', 'Fecha de la última calibración (Unix Timestamp- UTC).', 'R', '16 bits', NULL),
(9, 8, 'HR_TS_CALIB1 ', 'Fecha de la última calibración (Unix Timestamp- UTC).', 'R', '16 bits', NULL),
(10, 9, 'HR_TS_CALIB2 ', 'Fecha de la última calibración (Unix Timestamp- UTC).', 'R', '16 bits', NULL),
(11, 10, 'HR_TS_CALIB3 ', 'Fecha de la última calibración (Unix Timestamp- UTC).', 'R', '16 bits', NULL),
(12, 11, 'HR_VERSAO_FW ', 'Versión de firmware.', 'R', '16 bits', NULL),
(13, 12, 'HR_ID    ', 'Código de identificación: 0x0300 (hexadecimal).', 'R', '16 bits', NULL),
(14, 14, 'HR_AI1_LO  ', 'Valor leído de la entrada A1.', 'R', '16 bits', NULL),
(15, 15, 'HR_AI1_HI  ', 'Valor leído de la entrada A1.', 'R', '16 bits', NULL),
(16, 16, 'HR_AI2_LO  ', 'Valor leído de la entrada A2.', 'R', '16 bits', NULL),
(17, 17, 'HR_AI2_HI  ', 'Valor leído de la entrada A2.', 'R', '16 bits', NULL),
(18, 18, 'HR_AO1_LO  ', 'Valor actual de la salida O1.', 'R', '16 bits', NULL),
(19, 19, 'HR_AO1_HI  ', 'Valor actual de la salida O1.', 'R', '16 bits', NULL),
(20, 20, 'HR_AO2_LO  ', 'Valor actual de la salida O2.', 'R', '16 bits', NULL),
(21, 21, 'HR_AO2_HI  ', 'Valor actual de la salida O2.', 'R', '16 bits', NULL),
(22, 22, 'HR_COUNTER1_LO', 'Valor actual del contador de la entrada D1.', 'R', '16 bits', '0'),
(23, 23, 'HR_COUNTER1_HI', 'Valor actual del contador de la entrada D1.', 'R', '16 bits', '0'),
(24, 24, 'HR_COUNTER2_LO', 'Valor actual del contador de la entrada D2.', 'R', '16 bits', '0'),
(25, 25, 'HR_COUNTER2_HI', 'Valor actual del contador de la entrada D2.', 'R', '16 bits', '0'),
(26, 26, 'HR_COUNTER3_LO', 'Valor actual del contador de la entrada D3.', 'R', '16 bits', '0'),
(27, 27, 'HR_COUNTER3_HI', 'Valor actual del contador de la entrada D3.', 'R', '16 bits', '0'),
(28, 28, 'HR_COUNTER4_LO', 'Valor actual del contador de la entrada D4.', 'R', '16 bits', '0'),
(29, 29, 'HR_COUNTER4_HI', 'Valor actual del contador de la entrada D4.', 'R', '16 bits', '0'),
(30, 30, 'HR_COUNTER5_LO', 'Valor actual del contador de la entrada D5.', 'R', '16 bits', NULL),
(31, 31, 'HR_COUNTER5_HI', 'Valor actual del contador de la entrada D5.', 'R', '16 bits', NULL),
(32, 32, 'HR_COUNTER6_LO', 'Valor actual del contador de la entrada D6.', 'R', '16 bits', NULL),
(33, 33, 'HR_COUNTER6_HI', 'Valor actual del contador de la entrada D6.', 'R', '16 bits', NULL),
(34, 34, 'HR_COUNTER7_LO', 'Valor actual del contador de la entrada D7.', 'R', '16 bits', NULL),
(35, 35, 'HR_COUNTER7_HI', 'Valor actual del contador de la entrada D7.', 'R', '16 bits', NULL),
(36, 36, 'HR_COUNTER8_LO', 'Valor actual del contador de la entrada D8.', 'R', '16 bits', NULL),
(37, 37, 'HR_COUNTER8_HI', 'Valor actual del contador de la entrada D8.', 'R', '16 bits', NULL),
(38, 38, 'HR_DI1_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D1.', 'R', '16 bits', NULL),
(39, 39, 'HR_DI1_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D1.', 'R', '16 bits', NULL),
(40, 40, 'HR_DI2_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D2.', 'R', '16 bits', NULL),
(41, 41, 'HR_DI2_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D2.', 'R', '16 bits', NULL),
(42, 42, 'HR_DI3_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D3.', 'R', '16 bits', NULL),
(43, 43, 'HR_DI3_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D3.', 'R', '16 bits', NULL),
(44, 44, 'HR_DI4_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D4.', 'R', '16 bits', NULL),
(45, 45, 'HR_DI4_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D4.', 'R', '16 bits', NULL),
(46, 46, 'HR_DI5_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D5.', 'R', '16 bits', NULL),
(47, 47, 'HR_DI5_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D5.', 'R', '16 bits', NULL),
(48, 48, 'HR_DI6_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D6.', 'R', '16 bits', NULL),
(49, 49, 'HR_DI6_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D6.', 'R', '16 bits', NULL),
(50, 50, 'HR_DI7_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D7.', 'R', '16 bits', NULL),
(51, 51, 'HR_DI7_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D7.', 'R', '16 bits', NULL),
(52, 52, 'HR_DI8_TIME_ON_LO ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D8.', 'R', '16 bits', NULL),
(53, 53, 'HR_DI8_TIME_ON_HI ', 'Valor actual del integrador de tiempo \"ON\" de la entrada D8.', 'R', '16 bits', NULL),
(54, 54, 'HR_DI1_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D1.', 'R', '16 bits', NULL),
(55, 55, 'HR_DI1_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D1.', 'R', '16 bits', NULL),
(56, 56, 'HR_DI2_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D2.', 'R', '16 bits', NULL),
(57, 57, 'HR_DI2_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D2.', 'R', '16 bits', NULL),
(58, 58, 'HR_DI3_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D3.', 'R', '16 bits', NULL),
(59, 59, 'HR_DI3_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D3.', 'R', '16 bits', NULL),
(60, 60, 'HR_DI4_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D4.', 'R', '16 bits', NULL),
(61, 61, 'HR_DI4_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D4.', 'R', '16 bits', NULL),
(62, 62, 'HR_DI5_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D5.', 'R', '16 bits', NULL),
(63, 63, 'HR_DI5_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D5.', 'R', '16 bits', NULL),
(64, 64, 'HR_DI6_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D6.', 'R', '16 bits', NULL),
(65, 65, 'HR_DI6_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D6.', 'R', '16 bits', NULL),
(66, 66, 'HR_DI7_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D7.', 'R', '16 bits', NULL),
(67, 67, 'HR_DI7_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D7.', 'R', '16 bits', NULL),
(68, 68, 'HR_DI8_TIME_OFF_LO ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D8.', 'R', '16 bits', NULL),
(69, 69, 'HR_DI8_TIME_OFF_HI ', 'Valor actual del integrador de tiempo \"OFF\" de la entrada D8.', 'R', '16 bits', NULL),
(70, 70, 'HR_INPUT1_STATE  ', 'Estado de la entrada D1.', 'R', 'bit / 16 bits', '0'),
(71, 71, 'HR_INPUT2_STATE  ', 'Estado de la entrada D2.', 'R', 'bit / 16 bits', '0'),
(72, 72, 'HR_INPUT3_STATE  ', 'Estado de la entrada D3.', 'R', 'bit / 16 bits', '0'),
(73, 73, 'HR_INPUT4_STATE  ', 'Estado de la entrada D4.', 'R', 'bit / 16 bits', '0'),
(74, 74, 'HR_INPUT5_STATE  ', 'Estado de la entrada D5.', 'R', 'bit / 16 bits', NULL),
(75, 75, 'HR_INPUT6_STATE  ', 'Estado de la entrada D6.', 'R', 'bit / 16 bits', NULL),
(76, 76, 'HR_INPUT7_STATE  ', 'Estado de la entrada D7.', 'R', 'bit / 16 bits', NULL),
(77, 77, 'HR_INPUT8_STATE  ', 'Estado de la entrada D8.', 'R', 'bit / 16 bits', NULL),
(78, 78, 'HR_OUTPUT1_STATE  ', 'Estado actual de la salida K1/R1.', 'R', 'bit / 16 bits', NULL),
(79, 79, 'HR_OUTPUT2_STATE  ', 'Estado actual de la salida K2/R2.', 'R', 'bit / 16 bits', NULL),
(80, 80, 'HR_OUTPUT3_STATE  ', 'Estado actual de la salida K3/R3.', 'R', 'bit / 16 bits', NULL),
(81, 81, 'HR_OUTPUT4_STATE  ', 'Estado actual de la salida K4/R4.', 'R', 'bit / 16 bits', NULL),
(82, 82, 'HR_OUTPUT5_STATE  ', 'Estado actual de la salida K5.', 'R', 'bit / 16 bits', NULL),
(83, 83, 'HR_OUTPUT6_STATE  ', 'Estado actual de la salida K6.', 'R', 'bit / 16 bits', NULL),
(84, 84, 'HR_OUTPUT7_STATE  ', 'Estado actual de la salida K7.', 'R', 'bit / 16 bits', NULL),
(85, 85, 'HR_OUTPUT8_STATE  ', 'Estado actual de la salida K8.', 'R', 'bit / 16 bits', NULL),
(86, 94, 'HR_INTERNAL_TEMP  ', 'Valor de temperatura de la Junta Fría', 'R', '16 bits', NULL),
(87, 98, 'HR_STATUS_AI_CH1  ', 'LED de estado del canal A1.', 'R', '16 bits', NULL),
(88, 99, 'HR_STATUS_AI_CH2  ', 'LED de estado del canal A2.', 'R', '16 bits', NULL),
(89, 132, 'HR_INFO_ETH_IPV4_LO   ', 'Dirección IPv4.', 'R', '16 bits', NULL),
(90, 133, 'HR_INFO_ETH_IPv4_HI   ', 'Dirección IPv4.', 'R', '16 bits', NULL),
(91, 134, 'HR_INFO_ETH_IPV4_SBNT_MSK_LO ', 'Máscara de subred IPv4 .', 'R', '16 bits', NULL),
(92, 135, 'HR_INFO_ETH_IPV4_SBNT_MSK_HI ', 'Máscara de subred IPv4', 'R', '16 bits', NULL),
(93, 136, 'HR_INFO_ETH_IPV4_DFLT_GTWY_LO ', 'Gateway IPv4 (Mismo formato de la dirección IP).', 'R', '16 bits', NULL),
(94, 137, 'HR_INFO_ETH_IPV4_DFLT_GTWY_HI ', 'Gateway IPv4', 'R', '16 bits', NULL),
(95, 140, 'HR_TOTAL_SOCKETS    ', 'Número de sockets disponibles.', 'R', '16 bits', NULL),
(96, 141, 'HR_SOCKETS_IN_USE    ', 'Número de sockets en utilización.', 'R', '16 bits', NULL),
(97, 142, 'HR_GENERAL_ERROR_LO   ', 'Contador de errores de la interfaz Ethernet.', 'R', '16 bits', NULL),
(98, 143, 'HR_GENERAL_ERROR_HI   ', 'Contador de errores de la interfaz Ethernet.', 'R', '16 bits', NULL),
(99, 144, 'HR_RELISTEN_ERROR_LO  ', 'Contador de errores de relisten.', 'R', '16 bits', NULL),
(100, 145, 'HR_RELISTEN_ERROR_HI  ', 'Contador de errores de relisten.', 'R', '16 bits', NULL),
(101, 146, 'HR_SOCKET_SWITCH_ERROR_LO', 'Contador de errores de conmutación de los sockets.', 'R', '16 bits', NULL),
(102, 147, 'HR_SOCKET_SWITCH_ERROR_HI', 'Contador de errores de conmutación de los sockets.', 'R', '16 bits', NULL),
(103, 148, 'HR_DISCONNECT_ERROR_LO ', 'Contador de errores de desconexión.', 'R', '16 bits', NULL),
(104, 149, 'HR_DISCONNECT_ERROR_HI ', 'Contador de errores de desconexión.', 'R', '16 bits', NULL),
(105, 150, 'HR_SOCKET_CREATION_ERROR_LO  ', 'Contador de errores de creación de sockets.', 'R', '16 bits', NULL),
(106, 151, 'HR_SOCKET_CREATION_ERROR_HI  ', 'Contador de errores de creación de sockets.', 'R', '16 bits', NULL),
(107, 152, 'HR_SOCKET_DELETE_ERROR_LO', 'Contador de errores de sockets borrados.', 'R', '16 bits', NULL),
(108, 153, 'HR_SOCKET_DELETE_ERROR_HI', 'Contador de errores de sockets borrados.', 'R', '16 bits', NULL),
(109, 154, 'HR_IP_INVALID_PACKETS_LO', 'Número de paquetes no válidos recibidos.', 'R', '16 bits', NULL),
(110, 155, 'HR_IP_INVALID_PACKETS_HI', 'Número de paquetes no válidos recibidos.', 'R', '16 bits', NULL),
(111, 156, 'HR_PACKETS_SENT_LO   ', 'Número de paquetes enviados.', 'R', '16 bits', NULL),
(112, 157, 'HR_PACKETS_SENT_HI   ', 'Número de paquetes enviados.', 'R', '16 bits', NULL),
(113, 158, 'HR_PACKETS_RECEIVED_LO ', 'Número de paquetes recibidos.', 'R', '16 bits', NULL),
(114, 159, 'HR_PACKETS_RECEIVED_HI ', 'Número de paquetes recibidos.', 'R', '16 bits', NULL),
(115, 160, 'HR_ALLINPUTS_STATE   ', 'Concatena el estado de todas las entradas digitales', 'R', '16 bits', NULL),
(116, 162, 'HR_ALLOUTPUTS_STATE   ', 'Concatena el estado de todas las salidas digitales y relé', 'R', '16 bits', NULL),
(117, 500, 'HR_DO1_VALUE      ', 'Registro de manipulación del estado de la salida K1/R1.', 'R/W', '16 bits', NULL),
(118, 501, 'HR_DO2_VALUE      ', 'Registro de manipulación del estado de la salida K2/R2.', 'R/W', '16 bits', NULL),
(119, 502, 'HR_DO3_VALUE      ', 'Registro de manipulación del estado de la salida K3/R3.', 'R/W', '16 bits', NULL),
(120, 503, 'HR_DO4_VALUE      ', 'Registro de manipulación del estado de la salida K4/R4.', 'R/W', '16 bits', NULL),
(121, 504, 'HR_DO5_VALUE      ', 'Registro de manipulación del estado de la salida K5.', 'R/W', '16 bits', NULL),
(122, 505, 'HR_DO6_VALUE      ', 'Registro de manipulación del estado de la salida K6.', 'R/W', '16 bits', NULL),
(123, 506, 'HR_DO7_VALUE      ', 'Registro de manipulación del estado de la salida K7.', 'R/W', '16 bits', NULL),
(124, 507, 'HR_DO8_VALUE      ', 'Registro de manipulación del estado de la salida K8.', 'R/W', '16 bits', NULL),
(125, 508, 'HR_DO1_STATE_TO_FORCE  ', 'Valor al forzar la salida K1/R1.', 'R/W', '16 bits', NULL),
(126, 509, 'HR_DO1_FORCE_STATE   ', 'Permite forzar la salida K1/R1.', 'R/W', '16 bits', NULL),
(127, 510, 'HR_DO2_STATE_TO_FORCE  ', 'Valor al forzar la salida K2/R2.', 'R/W', '16 bits', NULL),
(128, 511, 'HR_DO2_FORCE_STATE   ', 'Permite forzar la salida K2/R2.', 'R/W', '16 bits', NULL),
(129, 512, 'HR_DO3_STATE_TO_FORCE  ', 'Valor al forzar la salida K3/R3.', 'R/W', '16 bits', NULL),
(130, 513, 'HR_DO3_FORCE_STATE   ', 'Permite forzar la salida K3/R3.', 'R/W', '16 bits', NULL),
(131, 514, 'HR_DO4_STATE_TO_FORCE  ', 'Valor al forzar la salida K4/R4.', 'R/W', '16 bits', NULL),
(132, 515, 'HR_DO4_FORCE_STATE   ', 'Permite forzar la salida K4/R4.', 'R/W', '16 bits', NULL),
(133, 516, 'HR_DO5_STATE_TO_FORCE  ', 'Valor al forzar la salida K5.', 'R/W', '16 bits', NULL),
(134, 517, 'HR_DO5_FORCE_STATE   ', 'Permite forzar la salida K5.', 'R/W', '16 bits', NULL),
(135, 518, 'HR_DO6_STATE_TO_FORCE  ', 'Valor al forzar la salida K6.', 'R/W', '16 bits', NULL),
(136, 519, 'HR_DO6_FORCE_STATE   ', 'Permite forzar la salida K6.', 'R/W', '16 bits', NULL),
(137, 520, 'HR_DO7_STATE_TO_FORCE  ', 'Valor al forzar la salida K7.', 'R/W', '16 bits', NULL),
(138, 521, 'HR_DO7_FORCE_STATE   ', 'Permite forzar la salida K7.', 'R/W', '16 bits', NULL),
(139, 522, 'HR_DO8_STATE_TO_FORCE  ', 'Valor al forzar la salida K8.', 'R/W', '16 bits', NULL),
(140, 523, 'HR_DO8_FORCE_STATE   ', 'Permite forzar la salida K8.', 'R/W', '16 bits', NULL),
(141, 524, 'HR_AO1_VALUE      ', 'Registro de manipulación de valores aplicados por la salida O1.', 'R/W', '16 bits', NULL),
(142, 525, 'HR_AO2_VALUE      ', 'Registro de manipulación de valores aplicados por la salida O2.', 'R/W', '16 bits', NULL),
(143, 526, 'HR_AO1_VALUE_TO_FORCE  ', 'Valor al forzar la salida O1.', 'R/W', '16 bits', NULL),
(144, 527, 'HR_AO1_FORCE_VALUE   ', 'Permite forzar la salida O1.', 'R/W', '16 bits', NULL),
(145, 528, 'HR_AO2_VALUE_TO_FORCE  ', 'Valor al forzar la salida O2.', 'R/W', '16 bits', NULL),
(146, 529, 'HR_AO2_FORCE_VALUE   ', 'Permite forzar la salida O2.', 'R/W', '16 bits', NULL),
(147, 530, 'HR_DOALL_VALUE     ', 'Registro de manejo concatenado sobre el estado de todas las salidas digitales y de relé (Kn/Rn).', 'R/W', '16 bits', NULL),
(148, 1530, 'HR_DI1_FORCE_LO    ', 'Valor al forzar la entrada D1.', 'R/W', '16 bits', NULL),
(149, 1531, 'HR_DI1_FORCE_HI    ', 'Valor al forzar la entrada D1.', 'R/W', '16 bits', NULL),
(150, 1533, 'HR_DI1_FORCE      ', 'Permite forzar la entrada D1.', 'R/W', '16 bits', NULL),
(151, 1580, 'HR_DI2_FORCE_LO    ', 'Valor al forzar la entrada D2.', 'R/W', '16 bits', NULL),
(152, 1581, 'HR_DI2_FORCE_HI    ', 'Valor al forzar la entrada D2.', 'R/W', '16 bits', NULL),
(153, 1583, 'HR_DI2_FORCE      ', 'Permite forzar la entrada D2.', 'R/W', '16 bits', NULL),
(154, 1630, 'HR_DI3_FORCE_LO    ', 'Valor al forzar la entrada D3.', 'R/W', '16 bits', NULL),
(155, 1631, 'HR_DI3_FORCE_HI    ', 'Valor al forzar la entrada D3.', 'R/W', '16 bits', NULL),
(156, 1633, 'HR_DI3_FORCE      ', 'Permite forzar la entrada D3.', 'R/W', '16 bits', NULL),
(157, 1680, 'HR_DI4_FORCE_LO    ', 'Valor al forzar la entrada D4.', 'R/W', '16 bits', NULL),
(158, 1681, 'HR_DI4_FORCE_HI    ', 'Valor al forzar la entrada D4.', 'R/W', '16 bits', NULL),
(159, 1683, 'HR_DI4_FORCE      ', 'Permite forzar la entrada D4.', 'R/W', '16 bits', NULL),
(160, 1730, 'HR_DI5_FORCE_LO    ', 'Valor al forzar la entrada D5.', 'R/W', '16 bits', NULL),
(161, 1731, 'HR_DI5_FORCE_HI    ', 'Valor al forzar la entrada D5.', 'R/W', '16 bits', NULL),
(162, 1733, 'HR_DI5_FORCE      ', 'Permite forzar la entrada D5.', 'R/W', '16 bits', NULL),
(163, 1780, 'HR_DI6_FORCE_LO    ', 'Valor al forzar la entrada D6.', 'R/W', '16 bits', NULL),
(164, 1781, 'HR_DI6_FORCE_HI    ', ' Valor al forzar la entrada D6.', 'R/W', '16 bits', NULL),
(165, 1783, 'HR_DI6_FORCE      ', 'Permite forzar la entrada D6.', 'R/W', '16 bits', NULL),
(166, 1830, 'HR_DI7_FORCE_LO    ', 'Valor al forzar la entrada D7.', 'R/W', '16 bits', NULL),
(167, 1831, 'HR_DI7_FORCE_HI    ', 'Valor al forzar la entrada D7.', 'R/W', '16 bits', NULL),
(168, 1833, 'HR_DI7_FORCE      ', 'Permite forzar la entrada D7.', 'R/W', '16 bits', NULL),
(169, 1880, 'HR_DI8_FORCE_LO    ', 'Valor al forzar la entrada D8.', 'R/W', '16 bits', NULL),
(170, 1881, 'HR_DI8_FORCE_HI    ', 'Valor al forzar la entrada D8.', 'R/W', '16 bits', NULL),
(171, 1883, 'HR_DI8_FORCE      ', 'Permite forzar la entrada D8.', 'R/W', '16 bits', NULL),
(172, 2333, 'HR_AI1_FORCE_VALUE   ', 'Permite forzar la entrada A1.', 'R/W', '16 bits', NULL),
(173, 2334, 'HR_AI1_FORCED_LO    ', 'Valor al forzar la entrada A1 (32 bits).', 'R/W', '16 bits', NULL),
(174, 2335, 'HR_AI1_FORCED_HI    ', 'Valor al forzar la entrada A1 (32 bits).', 'R/W', '16 bits', NULL),
(175, 2383, 'HR_AI2_FORCE_VALUE   ', 'Permite forzar la entrada A2.', 'R/W', '16 bits', NULL),
(176, 2384, 'HR_AI2_FORCED_LO    ', 'Valor al forzar la entrada A2 (32 bits).', 'R/W', '16 bits', NULL),
(177, 2385, 'HR_AI2_FORCED_HI    ', 'Valor al forzar la entrada A2 (32 bits).', 'R/W', '16 bits', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `registros_modbus`
--
ALTER TABLE `registros_modbus`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `registros_modbus`
--
ALTER TABLE `registros_modbus`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=178;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
