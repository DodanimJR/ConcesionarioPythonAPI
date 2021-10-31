-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 31, 2021 at 11:44 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Concesionario`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `cedula` int(11) NOT NULL,
  `tipoCedula` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `calificacionCredito` int(3) NOT NULL,
  `residencia` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `birthdate` varchar(255) NOT NULL,
  `civ` int(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`cedula`, `tipoCedula`, `nombre`, `apellido`, `calificacionCredito`, `residencia`, `telefono`, `birthdate`, `civ`) VALUES
(118780115, 'TSE', 'Patrick', 'Flores', 100, 'Alajuela, Alajuela', '+506 6093-1439', '24/06/2000', 1000002),
(118780119, 'TSE', 'Paco', 'Picapiedra', 90, 'Itiqis, Alajuela', '+506 6093-1440', '24/06/1998', 1000002),
(118790116, 'TSE', 'Dodanim', 'Castillo Flores', 100, 'La Ceiba, Alajuela', '+506 6093-1438', '24/06/2003', 1000001);

-- --------------------------------------------------------

--
-- Table structure for table `vendedores`
--

CREATE TABLE `vendedores` (
  `civ` int(7) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `birthdate` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `salario` int(11) NOT NULL,
  `residencia` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `porcentajeDeComision` int(3) NOT NULL,
  `montoDeComision` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vendedores`
--

INSERT INTO `vendedores` (`civ`, `nombre`, `apellido`, `birthdate`, `tipo`, `salario`, `residencia`, `telefono`, `porcentajeDeComision`, `montoDeComision`) VALUES
(1000001, 'Rodolfo', 'Benavides', '12/06/1994', 'Especialista en sedanes', 600000, 'Tambor,Alajuela,Costa Rica', '+506 1234-5678', 6, 0),
(1000002, 'Pedro', 'Perez', '15/07/1995', 'Especialista en SUV\'S', 500000, 'La ceiba,Alajuela', '+506 1243-5678', 5, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ventas`
--

CREATE TABLE `ventas` (
  `cuv` int(11) NOT NULL,
  `codigoConsecutivo` varchar(255) NOT NULL,
  `numeroContrato` varchar(255) NOT NULL,
  `civ` int(7) NOT NULL,
  `cedulaCliente` int(11) NOT NULL,
  `monto` int(11) NOT NULL,
  `fechaVenta` varchar(255) NOT NULL,
  `producto` varchar(255) NOT NULL,
  `marca` varchar(255) NOT NULL,
  `modelo` varchar(255) NOT NULL,
  `year` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ventas`
--

INSERT INTO `ventas` (`cuv`, `codigoConsecutivo`, `numeroContrato`, `civ`, `cedulaCliente`, `monto`, `fechaVenta`, `producto`, `marca`, `modelo`, `year`) VALUES
(1, '180000023000001', 'CR-FTA-2021-31-10', 1000001, 118790116, 5650000, '31/10/2021', 'SEDAN', 'TOYOTA', 'Corolla', 2021),
(3, '180000023000002', 'CR-FTA-2021-31-11', 1000002, 118780119, 10000000, '26/11/2021', 'SEDAN', 'NISSAN', '10000000', 2021);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`cedula`),
  ADD KEY `civ` (`civ`);

--
-- Indexes for table `vendedores`
--
ALTER TABLE `vendedores`
  ADD PRIMARY KEY (`civ`);

--
-- Indexes for table `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`cuv`),
  ADD KEY `civ` (`civ`),
  ADD KEY `cedula_cliente` (`cedulaCliente`),
  ADD KEY `cedulaCliente` (`cedulaCliente`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ventas`
--
ALTER TABLE `ventas`
  MODIFY `cuv` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`civ`) REFERENCES `vendedores` (`civ`);

--
-- Constraints for table `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`civ`) REFERENCES `vendedores` (`civ`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`cedulaCliente`) REFERENCES `clientes` (`cedula`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
