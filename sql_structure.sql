/*
SQLyog Community v12.3.1 (64 bit)
MySQL - 8.0.32 : Database - product_db
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`product_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `product_db`;

/*Table structure for table `cart` */
DROP TABLE IF EXISTS `product_db`.`cart`;
CREATE TABLE `cart` (
  `name` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `total` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `cart` */

/*Table structure for table `product` */
DROP TABLE IF EXISTS `product_db`.`product`;
CREATE TABLE `product_db`.`product` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `stock` int DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `product` */

INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('1', 'Dell Inspiron', 'Work', '50000', '100');
INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('2', 'HP Omen', 'Gaming', '85000', '75');
INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('3', 'Asus ROG', 'Gaming', '80000', '50');
INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('4', 'Acer Aspire 5', 'Work', '70000', '0');
INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('5', 'Asus Chromebook', 'Work', '55000', '50');
INSERT INTO `product_db`.`product` (`pid`, `name`, `category`, `price`, `stock`) VALUES ('6', 'Asus TUF', 'Gaming', '60000', '50');


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
