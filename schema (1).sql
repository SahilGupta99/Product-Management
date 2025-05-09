CREATE DATABASE  IF NOT EXISTS `product_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `product_management`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: product_management
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (21,'Prefabricated House','AMS Enterprises extensive range of Wooden House is manufactured using superior quality panels and other raw materials that ensure its robustness and long life. Farm houses are prepared with high grade steel, CFB, EPS, and PUF panels that are procured from our trusted and consistent merchant due to the assiduous efforts of our brilliant professionals. We are proficient to offer an extensive collection of portable farm houses in vary designs to our respected customers. Consumers can avail this farm house from us according to their specifications at the industry leading price.','/static/uploads/categories/category_1745398081_virtualshowroom.png'),(22,'Portable House','AMS Enterprises extensive range of Portable House is manufactured using superior quality panels and other rawmaterials that ensure its robustness and long life. Farm houses are prepared with high grade steel, CFB, EPS, and PUFpanels that are procured from our trusted and consistent merchant due to the assiduous efforts of our brilliantprofessionals. We are proficient to offer an extensive collection of portable farm houses in vary designs to our respected customers.Consumers can avail this farm house from us according to their specifications at the','/static/uploads/categories/category_1745398105_karsten-wurth-7BjhtdogU3A-unsplash.jpg'),(23,'Portable Cabin AMS Group','Service Provider of a wide range of services which include ms porta cabin, 15 x10 feet wooden portable cabin, 10x10 feet ms porta cabin, porta cabin manufacturers in delhi, porta cabin in chandigarh and porta cabin in dehradun.','/static/uploads/categories/category_1745398117_zoltan-tasi-sJGvoX_eVhw-unsplash.jpg');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `requirement` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (12,'sahil','sahil.sg9971@gmail.com','+1 234 567 8900','a','a','Personal Use Requirement','d','127.0.0.1','2025-05-08 10:03:51'),(13,'sahil','sahil.sg9971@gmail.com','+1 234 567 8900','a','s','Personal Use Requirement','d','127.0.0.1','2025-05-08 10:04:14'),(14,'sahil','sahil.sg9971@gmail.com','+1 234 567 8900','a','a','Hotel Resort Project','s','127.0.0.1','2025-05-08 10:05:13'),(15,'sahil','sahil.sg9971@gmail.com','+1 234 567 8900','a','a','Hotel Resort Project','d','127.0.0.1','2025-05-08 10:05:37'),(16,'sahil','sahil.sg9971@gmail.com','+1 234 567 8900','s','a','Farm house Project','s','127.0.0.1','2025-05-08 10:06:38');
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `specs` json DEFAULT NULL,
  `image_urls` json DEFAULT NULL,
  `video_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (7,21,'Wooden Frame Houses','This is a farm houses ',1400.00,'\"{\\\"Ground Floor Dimensions\\\": \\\"Ground Floor\\\", \\\"Ground floor Area\\\": \\\"1000 Sq ft\\\", \\\"Material\\\": \\\"Steel\\\", \\\"Minimum order quantity\\\": \\\"1000 sq ft\\\", \\\"Place of Origin\\\": \\\"Pan India\\\", \\\"size\\\": \\\"500 Sq ft\\\"}\"','\"/static/uploads/A-1.jpg,/static/uploads/A-2.jpg,/static/uploads/A-3.jpg,/static/uploads/A-4.jpg,/static/uploads/A-5.jpg\"',''),(8,21,'Wooden Modular Prefabricated Cottage','Prefabricated houses, or prefab houses, are homes constructed using factory-made components or modules that are then assembled on-site. These components, which can include walls, floors, and roofing,',1400.00,'{\"size\": \"500 Sq ft\", \"Material\": \"Steel\", \"Place of Origin\": \"Pan India\", \"Ground floor Area\": \"1000 Sq ft\", \"Minimum order quantity\": \"1000 sq ft\", \"Ground Floor Dimensions\": \"Ground Floor\"}','\"/static/uploads/1.jpg,/static/uploads/2.jpg,/static/uploads/3.jpeg,/static/uploads/4.jpeg,/static/uploads/5.jpg\"',''),(9,22,'Rectangular Portable Houses','Prefabricated houses, or prefab houses, are homes constructed using factory-made components or modules that are then assembled on-site. These components, which can include walls, floors, and roofing,',1400.00,'{\"Color\": \"grey\", \"Shape\": \"Rectangular\", \"Material\": \"Mild Steel\", \"Build Type\": \"Panel Build\", \"Window Type\": \"Aluminium\", \"Usage/Application\": \"House\"}','\"/static/uploads/6.jpg,/static/uploads/7.jpg,/static/uploads/8.jpg,/static/uploads/9.jpg\"',''),(10,23,'Rectangular Portable Houses','Prefabricated houses, or prefab houses, are homes constructed using factory-made components or modules that are then assembled on-site. These components, which can include walls, floors, and roofing,',1400.00,'{\"Color\": \"grey\", \"Material\": \"Mild Steel\", \"Is It Portable\": \"No\", \"Country of Origin\": \"Made in India\", \"Is It Customized\\t\": \"Yes\", \"Minimum order quantity\": \"1000 sq ft\"}','\"/static/uploads/6.jpg,/static/uploads/7.jpg,/static/uploads/8.jpg,/static/uploads/9.jpg\"',''),(11,21,'new product1','this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description this is description ',3213.00,'{\"none\": \"none\", \"Color\": \"none\", \"Material\": \"none\", \"Warranty\": \"none\"}','\"/static/uploads/michael-mouritz-WXX_DhjlmD4-unsplash.jpg,/static/uploads/pexels-eberhard-grossgasteiger-2098427.jpg,/static/uploads/pexels-lachlan-ross-6510344.jpg,/static/uploads/pexels-guilherme-rossi-1755683.jpg,/static/uploads/pexels-aleksandar-pasaric-2603464.jpg\"','/static/uploads/productvideo.mp4'),(12,22,'sahil','this is the description',654.00,'{\"none\": \"none\", \"Color\": \"none\", \"Material\": \"none\", \"Warranty\": \"none\"}','\"/static/uploads/zoltan-tasi-sJGvoX_eVhw-unsplash.jpg,/static/uploads/jordon-conner-VIcTzkzNZR8-unsplash.jpg,/static/uploads/karsten-wurth-7BjhtdogU3A-unsplash.jpg,/static/uploads/michael-mouritz-WXX_DhjlmD4-unsplash.jpg,/static/uploads/pexels-eberhard-grossgasteiger-2098427.jpg\"','/static/uploads/istockphoto-1967534184-640_adpp_is.mp4');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-09 16:23:38
