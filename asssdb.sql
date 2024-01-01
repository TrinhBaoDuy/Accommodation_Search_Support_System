CREATE DATABASE  IF NOT EXISTS `asssdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `asssdb`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: asssdb
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `assss_booking`
--

DROP TABLE IF EXISTS `assss_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` int NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ASSSs_booking_post_id_e6814d8b_fk_ASSSs_post_id` (`post_id`),
  KEY `ASSSs_booking_user_id_e5ca6b1a_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `ASSSs_booking_post_id_e6814d8b_fk_ASSSs_post_id` FOREIGN KEY (`post_id`) REFERENCES `assss_post` (`id`),
  CONSTRAINT `ASSSs_booking_user_id_e5ca6b1a_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_booking`
--

LOCK TABLES `assss_booking` WRITE;
/*!40000 ALTER TABLE `assss_booking` DISABLE KEYS */;
INSERT INTO `assss_booking` VALUES (1,1,1,54,1,'2023-12-28','2023-12-28',NULL),(2,1,5,54,1,'2023-12-28','2023-12-28',NULL),(3,0,2,50,0,'2023-12-28','2023-12-28','2023-12-28 09:50:39.918467'),(4,0,2,54,1,'2023-12-28','2023-12-28',NULL),(5,0,5,54,1,'2023-12-28','2023-12-28',NULL),(6,0,4,54,1,'2023-12-28','2023-12-28',NULL),(7,0,3,54,1,'2023-12-28','2023-12-28',NULL),(8,0,3,54,1,'2023-12-28','2023-12-28',NULL),(9,0,3,54,1,'2023-12-28','2023-12-28',NULL),(10,0,3,54,1,'2023-12-28','2023-12-28',NULL);
/*!40000 ALTER TABLE `assss_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_comment`
--

DROP TABLE IF EXISTS `assss_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parentcomment_id` bigint DEFAULT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ASSSs_comment_parentcomment_id_d8d74d6b_fk_ASSSs_comment_id` (`parentcomment_id`),
  KEY `ASSSs_comment_post_id_374a6216_fk_ASSSs_post_id` (`post_id`),
  KEY `ASSSs_comment_user_id_cea7dda8_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `ASSSs_comment_parentcomment_id_d8d74d6b_fk_ASSSs_comment_id` FOREIGN KEY (`parentcomment_id`) REFERENCES `assss_comment` (`id`),
  CONSTRAINT `ASSSs_comment_post_id_374a6216_fk_ASSSs_post_id` FOREIGN KEY (`post_id`) REFERENCES `assss_post` (`id`),
  CONSTRAINT `ASSSs_comment_user_id_cea7dda8_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_comment`
--

LOCK TABLES `assss_comment` WRITE;
/*!40000 ALTER TABLE `assss_comment` DISABLE KEYS */;
INSERT INTO `assss_comment` VALUES (1,'hay qua',NULL,2,50,0,'2023-12-28','2023-12-28','2023-12-28 06:23:41.604780'),(2,'toi sua comment ne',NULL,2,50,1,'2023-12-28','2023-12-28',NULL),(3,'tra loi hay qua',NULL,1,51,1,'2023-12-28','2023-12-28',NULL),(4,'tra loi hay qua',1,1,51,1,'2023-12-28','2023-12-28',NULL),(5,'coment moi ne',NULL,1,49,1,'2023-12-28','2023-12-28',NULL),(6,'tra loi coment moi',4,1,50,1,'2023-12-28','2023-12-28',NULL);
/*!40000 ALTER TABLE `assss_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_discount`
--

DROP TABLE IF EXISTS `assss_discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_discount` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` double NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_discount`
--

LOCK TABLES `assss_discount` WRITE;
/*!40000 ALTER TABLE `assss_discount` DISABLE KEYS */;
INSERT INTO `assss_discount` VALUES (1,'',0,1,'2023-12-28','2023-12-28',NULL),(2,'SALE 10%',0.1,1,'2023-12-28','2023-12-28',NULL);
/*!40000 ALTER TABLE `assss_discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_follow`
--

DROP TABLE IF EXISTS `assss_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_follow` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `followeduser_id` bigint NOT NULL,
  `follower_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ASSSs_follow_followeduser_id_0c49883c_fk_ASSSs_user_id` (`followeduser_id`),
  KEY `ASSSs_follow_follower_id_7503e8f3_fk_ASSSs_user_id` (`follower_id`),
  CONSTRAINT `ASSSs_follow_followeduser_id_0c49883c_fk_ASSSs_user_id` FOREIGN KEY (`followeduser_id`) REFERENCES `assss_user` (`id`),
  CONSTRAINT `ASSSs_follow_follower_id_7503e8f3_fk_ASSSs_user_id` FOREIGN KEY (`follower_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_follow`
--

LOCK TABLES `assss_follow` WRITE;
/*!40000 ALTER TABLE `assss_follow` DISABLE KEYS */;
INSERT INTO `assss_follow` VALUES (1,51,50,1,'2023-12-26','2023-12-26',NULL),(2,52,54,1,'2023-12-26','2023-12-26',NULL),(3,52,50,1,'2023-12-26','2023-12-26',NULL),(4,50,53,1,'2023-12-26','2023-12-26',NULL),(5,54,50,0,'2023-12-27','2023-12-27','2023-12-27 12:22:20.822879');
/*!40000 ALTER TABLE `assss_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_house`
--

DROP TABLE IF EXISTS `assss_house`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_house` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `acreage` double NOT NULL,
  `price` double NOT NULL,
  `quantity` double NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_house`
--

LOCK TABLES `assss_house` WRITE;
/*!40000 ALTER TABLE `assss_house` DISABLE KEYS */;
INSERT INTO `assss_house` VALUES (1,'An Giang',1,10000,1,1,'2023-12-26','2023-12-26','2023-12-26 10:09:15.000000'),(2,'12',0,0,0,1,'2023-12-27','2023-12-27',NULL);
/*!40000 ALTER TABLE `assss_house` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_image`
--

DROP TABLE IF EXISTS `assss_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_image` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `imageURL` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `house_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ASSSs_image_house_id_4b7ce815_fk_ASSSs_house_id` (`house_id`),
  CONSTRAINT `ASSSs_image_house_id_4b7ce815_fk_ASSSs_house_id` FOREIGN KEY (`house_id`) REFERENCES `assss_house` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_image`
--

LOCK TABLES `assss_image` WRITE;
/*!40000 ALTER TABLE `assss_image` DISABLE KEYS */;
INSERT INTO `assss_image` VALUES (1,'image/upload/v1703686030/ASSS-house/rpozkqvd3v7vcryxyrml.jpg',1,1,'2023-12-27','2023-12-27',NULL),(2,'image/upload/v1703735488/ASSS-house/ffntjtpcxwciuyzmxqpx.jpg',1,1,'2023-12-28','2023-12-28',NULL);
/*!40000 ALTER TABLE `assss_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_post`
--

DROP TABLE IF EXISTS `assss_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `topic` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `describe` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `postingdate` datetime(6) DEFAULT NULL,
  `expirationdate` datetime(6) DEFAULT NULL,
  `status` int NOT NULL,
  `discount_id` bigint NOT NULL,
  `house_id` bigint NOT NULL,
  `postingprice_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ASSSs_post_discount_id_87584ff6_fk_ASSSs_discount_id` (`discount_id`),
  KEY `ASSSs_post_house_id_8bc55cb5_fk_ASSSs_house_id` (`house_id`),
  KEY `ASSSs_post_postingprice_id_6783a3cc_fk_ASSSs_postingprice_id` (`postingprice_id`),
  KEY `ASSSs_post_user_id_97763d14_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `ASSSs_post_discount_id_87584ff6_fk_ASSSs_discount_id` FOREIGN KEY (`discount_id`) REFERENCES `assss_discount` (`id`),
  CONSTRAINT `ASSSs_post_house_id_8bc55cb5_fk_ASSSs_house_id` FOREIGN KEY (`house_id`) REFERENCES `assss_house` (`id`),
  CONSTRAINT `ASSSs_post_postingprice_id_6783a3cc_fk_ASSSs_postingprice_id` FOREIGN KEY (`postingprice_id`) REFERENCES `assss_postingprice` (`id`),
  CONSTRAINT `ASSSs_post_user_id_97763d14_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_post`
--

LOCK TABLES `assss_post` WRITE;
/*!40000 ALTER TABLE `assss_post` DISABLE KEYS */;
INSERT INTO `assss_post` VALUES (1,'Cho thue tro Go Vap','nha cua rat tien nghi, gan truong dai hoc','2023-12-28 00:00:00.000000','2023-12-30 00:00:00.000000',0,1,1,1,51,1,'2023-12-28','2023-12-28',NULL),(2,'Nha tro Q7','vo cung tien nghi','2023-11-11 00:00:00.000000','2023-11-30 00:00:00.000000',1,1,1,1,51,0,'2023-12-28','2023-12-28','2023-12-28 05:29:02.756068'),(3,'Nha tro Q7','vo cung tien nghi','2023-12-11 00:00:00.000000','2023-12-30 00:00:00.000000',1,1,1,1,51,1,'2023-12-28','2023-12-28',NULL),(4,'Nha tro Q7','vo cung tien nghi','2023-11-11 00:00:00.000000','2023-12-30 00:00:00.000000',1,1,1,1,51,1,'2023-12-28','2023-12-28',NULL),(5,'Nha tro Q7','vo cung tien nghi','2023-12-29 00:00:00.000000','2023-12-30 00:00:00.000000',1,1,1,1,51,1,'2023-12-28','2023-12-28',NULL),(6,'Nha tro Q3','vo cung tien nghi','2023-12-28 00:00:00.000000','2023-12-30 00:00:00.000000',1,1,1,1,51,1,'2023-12-28','2023-12-28',NULL);
/*!40000 ALTER TABLE `assss_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_postingprice`
--

DROP TABLE IF EXISTS `assss_postingprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_postingprice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_postingprice`
--

LOCK TABLES `assss_postingprice` WRITE;
/*!40000 ALTER TABLE `assss_postingprice` DISABLE KEYS */;
INSERT INTO `assss_postingprice` VALUES (1,100000);
/*!40000 ALTER TABLE `assss_postingprice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_role`
--

DROP TABLE IF EXISTS `assss_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rolename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rolename` (`rolename`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_role`
--

LOCK TABLES `assss_role` WRITE;
/*!40000 ALTER TABLE `assss_role` DISABLE KEYS */;
INSERT INTO `assss_role` VALUES (1,'Admin'),(2,'Host'),(3,'User');
/*!40000 ALTER TABLE `assss_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_user`
--

DROP TABLE IF EXISTS `assss_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `address` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `phonenumber` double NOT NULL,
  `role_id` bigint DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created_date` date DEFAULT NULL,
  `updated_date` date DEFAULT NULL,
  `deleted_date` datetime(6) DEFAULT NULL,
  `gender` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `ASSSs_user_role_id_c479c720_fk_ASSSs_role_id` (`role_id`),
  CONSTRAINT `ASSSs_user_role_id_c479c720_fk_ASSSs_role_id` FOREIGN KEY (`role_id`) REFERENCES `assss_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_user`
--

LOCK TABLES `assss_user` WRITE;
/*!40000 ALTER TABLE `assss_user` DISABLE KEYS */;
INSERT INTO `assss_user` VALUES (49,'pbkdf2_sha256$600000$uH3U5A6ZB5peEUYy64dCHP$7Ol+ocAV7+PmGCLq8l+iHbD2a/XTMypYvpyZzZRkFZo=',NULL,0,'admin','John','Doe','john@example.com',0,1,'2023-12-26 08:07:05.121827','123 Main St',NULL,'1990-01-01',123456789,1,1,'2023-12-26','2023-12-27',NULL,NULL),(50,'pbkdf2_sha256$600000$oFTMohu6uPF7Cr7nquzwpf$Sg87KFZb/xARXu3fZM1jnxg8sozc1PYLNvSxzXTb8z8=',NULL,0,'jane_smith','Jane','Smith','jane@example.com',0,1,'2023-12-26 08:07:05.127761','456 Elm St','image/upload/v1703682425/ASSS-avatar/gt4k1ihyxyildaeagzqt.jpg','1995-05-10',987654321,3,1,'2023-12-26','2023-12-27',NULL,NULL),(51,'pbkdf2_sha256$600000$XCLqTg6Y9ICWpAcKM2qjlE$+WnJ+LXQykQciJpvvc3/mNTjwmW3pBEFSD8YiYMTLw0=',NULL,0,'host1','Host','One','host1@example.com',0,1,'2023-12-26 08:07:05.133212','123 Main St','','1990-01-01',111111111,2,1,'2023-12-26','2023-12-26',NULL,NULL),(52,'pbkdf2_sha256$600000$7rKOEtH5esXRyNI1Uvom01$d0kXlirbSqveGHstjNsqmbv65oFpIMJUMZQSaaDRZEM=',NULL,0,'host2','Host','Two','host2@example.com',0,1,'2023-12-26 08:07:05.137435','456 Elm St','','1990-02-02',222222222,2,1,'2023-12-26','2023-12-26',NULL,NULL),(53,'pbkdf2_sha256$600000$VWquw2Fp96csBjtjPRlCeC$drRRiipmHlNVRQYVmXbTCrwJke+FAg8emYu9NDm4HV4=',NULL,0,'host3','Host','Three','host3@example.com',0,1,'2023-12-26 08:07:05.143057','789 Oak St','','1990-03-03',333333333,2,1,'2023-12-26','2023-12-26',NULL,NULL),(54,'pbkdf2_sha256$600000$7rPArXy35MHgXyQBkaeiHX$EwncHaUF0mVgQJuO44jPC2X9hH9GG+SKU6T543jFglw=',NULL,0,'user1','User','One','user1@example.com',0,1,'2023-12-26 08:07:05.148269','123 Main St','','1995-01-01',444444444,3,1,'2023-12-26','2023-12-26',NULL,NULL),(55,'pbkdf2_sha256$600000$CQhilbZntxjhrSb143S4A2$RzYDeoCe4tl+ZTG1/CUiu+eB8aIWbX+ErMHMxMrEm3E=',NULL,0,'user2','User','Two','user2@example.com',0,1,'2023-12-26 08:07:05.155309','456 Elm St','','1995-02-02',555555555,3,1,'2023-12-26','2023-12-26',NULL,NULL),(56,'pbkdf2_sha256$600000$raIv8W907fSHI5wD6mZVBw$KC+Q8Q+Z1CM8SI4DoCUChPa7ekaKsTQDYs0kwg8oQU0=','2023-12-26 11:30:45.757925',1,'main','','','main@gmail.com',1,1,'2023-12-26 09:48:45.577354',NULL,NULL,NULL,0,NULL,1,'2023-12-26','2023-12-26',NULL,NULL),(57,'123',NULL,0,'duy1','trinh','duy','duy@gmail.com',0,1,'2023-12-26 11:14:13.617977','an giang','image/upload/v1703589257/i3vrvomkh0wrv8cgeio5.png','2002-11-16',123456789,2,1,'2023-12-26','2023-12-26',NULL,NULL),(58,'pbkdf2_sha256$600000$KAJQlLTHG8Y9L2NDR5FQjG$re+BXXxXG1oiZqqEv5ifVeEvChuQJ2UWfub4hBtKm8Q=',NULL,0,'duy13','trinh','duy','duy@gmail.com',0,1,'2023-12-26 11:16:17.654149','an giang','image/upload/v1703589381/jdtcyovpgsssvmftzlpg.png','2002-11-16',123456789,2,1,'2023-12-26','2023-12-26',NULL,NULL),(59,'pbkdf2_sha256$600000$oMJQZ6AZRyOVv3DbnlcXDZ$NTSlHlXBd5YP+TZFEr+tHuILMTZhj+DCr45RedbgvTU=',NULL,0,'duy3','trinh','duy','duy@gmail.com',0,1,'2023-12-26 11:24:08.346508','an giang','image/upload/v1703589851/o46mv8of1p1utlyd24jz.png','2002-11-16',123456789,2,1,'2023-12-26','2023-12-26',NULL,NULL),(60,'pbkdf2_sha256$600000$uTGH3jF80XIPCSQJkTR5dV$CdWPBHX26GmGZpeWnDUPl88f6prdGnkoJF+qgDBWwcg=',NULL,0,'nhap','Nguyen','Van Phuoc','2051050075duy@ou.edu.vn',0,1,'2023-12-26 11:30:50.000000','An Giang','image/upload/v1703590281/dfrdjtnrqzqr7noxf5ro.jpg','2023-12-01',388853371,2,1,'2023-12-26','2023-12-27',NULL,NULL),(61,'pbkdf2_sha256$600000$M16SjKSGBEJKuzLDb0Grbo$ifY3srrVKIECL4CWLcAXlo0df//hCrDDp6r8Kz/Q/do=',NULL,0,'duy5','trinh','duy','duy@gmail.com',0,1,'2023-12-26 11:36:32.445361','an giang','image/upload/v1703590596/ASSS-avatar/l1yjozj8inrzkhqqovvg.png','2002-11-16',123456789,2,1,'2023-12-26','2023-12-26',NULL,NULL),(62,'pbkdf2_sha256$600000$EbdkKEio7aEeJMtZho5Are$uZSJS8TDDuzkYcNaqaYoFShYQI9g2njxS5EkQ4AxR9Y=',NULL,0,'duy6','trinh','duy','duy@gmail.com',0,1,'2023-12-27 09:26:03.467975','an giang','image/upload/v1703669165/ASSS-avatar/acwuufmu7zmalmz3bwvw.png','2002-11-16',123456789,2,1,'2023-12-27','2023-12-27',NULL,NULL);
/*!40000 ALTER TABLE `assss_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_user_groups`
--

DROP TABLE IF EXISTS `assss_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ASSSs_user_groups_user_id_group_id_4b5fa6f1_uniq` (`user_id`,`group_id`),
  KEY `ASSSs_user_groups_group_id_de32b8bf_fk_auth_group_id` (`group_id`),
  CONSTRAINT `ASSSs_user_groups_group_id_de32b8bf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `ASSSs_user_groups_user_id_1b5a9982_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_user_groups`
--

LOCK TABLES `assss_user_groups` WRITE;
/*!40000 ALTER TABLE `assss_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `assss_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assss_user_user_permissions`
--

DROP TABLE IF EXISTS `assss_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assss_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ASSSs_user_user_permissions_user_id_permission_id_336e9f1e_uniq` (`user_id`,`permission_id`),
  KEY `ASSSs_user_user_perm_permission_id_76101ae7_fk_auth_perm` (`permission_id`),
  CONSTRAINT `ASSSs_user_user_perm_permission_id_76101ae7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `ASSSs_user_user_permissions_user_id_10dc3f80_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_user_user_permissions`
--

LOCK TABLES `assss_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `assss_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `assss_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add house',6,'add_house'),(22,'Can change house',6,'change_house'),(23,'Can delete house',6,'delete_house'),(24,'Can view house',6,'view_house'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Can add discount',8,'add_discount'),(30,'Can change discount',8,'change_discount'),(31,'Can delete discount',8,'delete_discount'),(32,'Can view discount',8,'view_discount'),(33,'Can add posting price',9,'add_postingprice'),(34,'Can change posting price',9,'change_postingprice'),(35,'Can delete posting price',9,'delete_postingprice'),(36,'Can view posting price',9,'view_postingprice'),(37,'Can add role',10,'add_role'),(38,'Can change role',10,'change_role'),(39,'Can delete role',10,'delete_role'),(40,'Can view role',10,'view_role'),(41,'Can add post',11,'add_post'),(42,'Can change post',11,'change_post'),(43,'Can delete post',11,'delete_post'),(44,'Can view post',11,'view_post'),(45,'Can add image',12,'add_image'),(46,'Can change image',12,'change_image'),(47,'Can delete image',12,'delete_image'),(48,'Can view image',12,'view_image'),(49,'Can add follow',13,'add_follow'),(50,'Can change follow',13,'change_follow'),(51,'Can delete follow',13,'delete_follow'),(52,'Can view follow',13,'view_follow'),(53,'Can add comment',14,'add_comment'),(54,'Can change comment',14,'change_comment'),(55,'Can delete comment',14,'delete_comment'),(56,'Can view comment',14,'view_comment'),(57,'Can add booking',15,'add_booking'),(58,'Can change booking',15,'change_booking'),(59,'Can delete booking',15,'delete_booking'),(60,'Can view booking',15,'view_booking'),(61,'Can add application',16,'add_application'),(62,'Can change application',16,'change_application'),(63,'Can delete application',16,'delete_application'),(64,'Can view application',16,'view_application'),(65,'Can add access token',17,'add_accesstoken'),(66,'Can change access token',17,'change_accesstoken'),(67,'Can delete access token',17,'delete_accesstoken'),(68,'Can view access token',17,'view_accesstoken'),(69,'Can add grant',18,'add_grant'),(70,'Can change grant',18,'change_grant'),(71,'Can delete grant',18,'delete_grant'),(72,'Can view grant',18,'view_grant'),(73,'Can add refresh token',19,'add_refreshtoken'),(74,'Can change refresh token',19,'change_refreshtoken'),(75,'Can delete refresh token',19,'delete_refreshtoken'),(76,'Can view refresh token',19,'view_refreshtoken'),(77,'Can add id token',20,'add_idtoken'),(78,'Can change id token',20,'change_idtoken'),(79,'Can delete id token',20,'delete_idtoken'),(80,'Can view id token',20,'view_idtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-12-26 10:09:28.884277','1','ID: 1, Address: An Giang, Price: 10000.0, Soluong: 1.0nguoi/phong, Dientich: 1.0m^2',1,'[{\"added\": {}}]',6,56),(2,'2023-12-26 11:31:19.912343','60','ID: 60, Name: Nguyen Van Phuoc, DOB: 2023-12-01, Email: 2051050075duy@ou.edu.vn, Address: An Giang, Role: Host',1,'[{\"added\": {}}]',7,56);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(15,'ASSSs','booking'),(14,'ASSSs','comment'),(8,'ASSSs','discount'),(13,'ASSSs','follow'),(6,'ASSSs','house'),(12,'ASSSs','image'),(11,'ASSSs','post'),(9,'ASSSs','postingprice'),(10,'ASSSs','role'),(7,'ASSSs','user'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(17,'oauth2_provider','accesstoken'),(16,'oauth2_provider','application'),(18,'oauth2_provider','grant'),(20,'oauth2_provider','idtoken'),(19,'oauth2_provider','refreshtoken'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-12-26 06:13:58.909563'),(2,'contenttypes','0002_remove_content_type_name','2023-12-26 06:13:59.067092'),(3,'auth','0001_initial','2023-12-26 06:13:59.816182'),(4,'auth','0002_alter_permission_name_max_length','2023-12-26 06:13:59.947552'),(5,'auth','0003_alter_user_email_max_length','2023-12-26 06:13:59.961061'),(6,'auth','0004_alter_user_username_opts','2023-12-26 06:13:59.973610'),(7,'auth','0005_alter_user_last_login_null','2023-12-26 06:13:59.989113'),(8,'auth','0006_require_contenttypes_0002','2023-12-26 06:13:59.994658'),(9,'auth','0007_alter_validators_add_error_messages','2023-12-26 06:14:00.003105'),(10,'auth','0008_alter_user_username_max_length','2023-12-26 06:14:00.017525'),(11,'auth','0009_alter_user_last_name_max_length','2023-12-26 06:14:00.030091'),(12,'auth','0010_alter_group_name_max_length','2023-12-26 06:14:00.052975'),(13,'auth','0011_update_proxy_permissions','2023-12-26 06:14:00.062947'),(14,'auth','0012_alter_user_first_name_max_length','2023-12-26 06:14:00.076331'),(15,'ASSSs','0001_initial','2023-12-26 06:14:00.627209'),(16,'ASSSs','0002_house_acreage_house_price_house_quantity','2023-12-26 06:14:00.706852'),(17,'ASSSs','0003_discount_postingprice_role_user_address_user_avatar_and_more','2023-12-26 06:14:02.837971'),(18,'ASSSs','0004_alter_user_avatar','2023-12-26 06:14:03.002338'),(19,'ASSSs','0005_alter_image_imageurl','2023-12-26 06:14:03.120157'),(20,'ASSSs','0006_alter_image_imageurl_alter_user_avatar','2023-12-26 06:14:03.379868'),(21,'ASSSs','0007_alter_booking_options_alter_comment_options_and_more','2023-12-26 06:14:04.710995'),(22,'admin','0001_initial','2023-12-26 06:14:04.902631'),(23,'admin','0002_logentry_remove_auto_add','2023-12-26 06:14:04.924683'),(24,'admin','0003_logentry_add_action_flag_choices','2023-12-26 06:14:04.947046'),(25,'sessions','0001_initial','2023-12-26 06:14:04.999754'),(26,'ASSSs','0008_booking_deleted_date_comment_deleted_date_and_more','2023-12-26 06:19:48.189390'),(27,'ASSSs','0009_alter_user_avatar','2023-12-26 08:49:31.092477'),(28,'ASSSs','0010_alter_user_avatar','2023-12-26 09:28:08.872287'),(29,'ASSSs','0011_alter_user_avatar','2023-12-26 09:28:57.286428'),(30,'ASSSs','0012_alter_user_avatar','2023-12-26 09:37:02.734596'),(31,'ASSSs','0013_alter_image_imageurl','2023-12-26 11:36:20.713997'),(32,'oauth2_provider','0001_initial','2023-12-26 15:11:04.331058'),(33,'oauth2_provider','0002_auto_20190406_1805','2023-12-26 15:11:04.427556'),(34,'oauth2_provider','0003_auto_20201211_1314','2023-12-26 15:11:04.498359'),(35,'oauth2_provider','0004_auto_20200902_2022','2023-12-26 15:11:05.137454'),(36,'oauth2_provider','0005_auto_20211222_2352','2023-12-26 15:11:05.267052'),(37,'oauth2_provider','0006_alter_application_client_secret','2023-12-26 15:11:05.316701'),(38,'oauth2_provider','0007_application_post_logout_redirect_uris','2023-12-26 15:11:05.420703'),(39,'ASSSs','0014_user_gender','2023-12-31 04:18:07.824129');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0xx1mjsop6983xsnjyje3erys05bkd67','.eJxVjDsOAjEMBe-SGkUhcT5Q0nOGle04ZAEl0n4qxN1hpS2gfTPzXmrAdanDOss0jFmdlQ_q8DsS8kPaRvId261r7m2ZRtKbonc662vP8rzs7t9Bxbl-6-QDuJI8OHI-WPDsCO3JRAFOKEcMiYClGPQGC7lIUqxwMBBZEJx6fwD6Wjhg:1rIPAe:3SkmUKwT6C3jraFObYamQCvuzBqhiIncpJgnEsyi4KE','2024-01-10 08:21:44.513514'),('wr9812im5wuwwk76vefbflk3qyzphnln','.eJxVjDsOAjEMBe-SGkUhcT5Q0nOGle04ZAEl0n4qxN1hpS2gfTPzXmrAdanDOss0jFmdlQ_q8DsS8kPaRvId261r7m2ZRtKbonc662vP8rzs7t9Bxbl-6-QDuJI8OHI-WPDsCO3JRAFOKEcMiYClGPQGC7lIUqxwMBBZEJx6fwD6Wjhg:1rI5e1:1zZaqbXZDQME2fzRW1ieYHImUKaNr3_sRjFflXkwHnc','2024-01-09 11:30:45.862288');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_provider_accesstoken`
--

DROP TABLE IF EXISTS `oauth2_provider_accesstoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_accesstoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `source_refresh_token_id` bigint DEFAULT NULL,
  `id_token_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `source_refresh_token_id` (`source_refresh_token_id`),
  UNIQUE KEY `id_token_id` (`id_token_id`),
  KEY `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr` FOREIGN KEY (`id_token_id`) REFERENCES `oauth2_provider_idtoken` (`id`),
  CONSTRAINT `oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr` FOREIGN KEY (`source_refresh_token_id`) REFERENCES `oauth2_provider_refreshtoken` (`id`),
  CONSTRAINT `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_accesstoken`
--

LOCK TABLES `oauth2_provider_accesstoken` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_accesstoken` DISABLE KEYS */;
INSERT INTO `oauth2_provider_accesstoken` VALUES (1,'AE7wPJ3SpMLhhUDPJc6yOlE1VzXylq','2023-12-27 01:33:37.075923','read write',1,49,'2023-12-26 15:33:37.076932','2023-12-26 15:33:37.076932',NULL,NULL),(2,'mrKbFT2fsOik3lXqMPgLzKQ09tKsmU','2023-12-27 02:44:14.992995','read write',1,49,'2023-12-26 16:44:14.992995','2023-12-26 16:44:14.992995',NULL,NULL),(3,'0zUAnnxKlrLtoNZ4zkcd1MnZpHSffJ','2023-12-27 16:18:14.207191','read write',1,49,'2023-12-27 06:18:14.207191','2023-12-27 06:18:14.207191',NULL,NULL),(4,'pi9BfHoO9phnv6XEZVoVC0RG64XX0F','2023-12-27 16:23:24.933117','read write',1,49,'2023-12-27 06:23:24.933117','2023-12-27 06:23:24.933117',NULL,NULL),(5,'KifwrOc6WHcuLxafr0cZ7FN9SbBPbW','2023-12-27 16:36:33.670172','read write',1,49,'2023-12-27 06:36:33.670172','2023-12-27 06:36:33.670172',NULL,NULL),(6,'Z9gbpSYIEUuip7wk1G62ay6kojMGWC','2023-12-27 19:04:48.190968','read write',1,50,'2023-12-27 09:04:48.191971','2023-12-27 09:04:48.191971',NULL,NULL),(7,'v9yeSWAdMCZfC0lDlEGgjjvE4n2yej','2023-12-27 19:57:02.374394','read write',1,50,'2023-12-27 09:57:02.375397','2023-12-27 09:57:02.375397',NULL,NULL),(8,'ofZXCQWuLQMEGKR3hf0j88GnElX6RT','2023-12-27 22:16:22.104039','read write',1,50,'2023-12-27 12:16:22.105691','2023-12-27 12:16:22.105691',NULL,NULL),(9,'PliyF1LlgyBvBefwoXld5noGk5PQy5','2023-12-28 17:01:53.028590','read write',1,50,'2023-12-28 07:01:53.029590','2023-12-28 07:01:53.029590',NULL,NULL),(10,'oD16aeV3qPsRfoUw8sF6hCRlFFBK36','2023-12-28 17:46:14.047304','read write',1,51,'2023-12-28 07:46:14.048304','2023-12-28 07:46:14.048304',NULL,NULL),(11,'uw9fug0D1DdNCVM2Eia1RSAW2zfneY','2023-12-28 17:47:46.216648','read write',1,54,'2023-12-28 07:47:46.217819','2023-12-28 07:47:46.217819',NULL,NULL),(12,'sRnKJWgGm24Wbx831sPh9y7rO7UxEB','2023-12-28 18:55:50.646526','read write',1,51,'2023-12-28 08:55:50.647657','2023-12-28 08:55:50.647657',NULL,NULL),(13,'e1BkViFLlxoVpJlyO5hMe9i0i7HswP','2023-12-28 19:13:21.815207','read write',1,50,'2023-12-28 09:13:21.816205','2023-12-28 09:13:21.816205',NULL,NULL),(14,'nkUZbByCn0hDqsw64FdKzv5Rrmq4Mi','2023-12-28 20:10:12.398621','read write',1,51,'2023-12-28 10:10:12.399618','2023-12-28 10:10:12.399618',NULL,NULL),(15,'2wMBzOafDx81n6tdH9TwBIfYOoHJPV','2023-12-31 15:39:04.809260','read write',1,51,'2023-12-31 05:39:04.809260','2023-12-31 05:39:04.809260',NULL,NULL),(16,'Ph9HCPuyifLy0prseTkuOWLK6zkGtc','2023-12-31 16:33:37.000462','read write',1,51,'2023-12-31 06:33:37.000462','2023-12-31 06:33:37.000462',NULL,NULL),(17,'X7C29gl7qaRrgYAY7bbvjdKP6UfMyJ','2024-01-01 17:43:00.140529','read write',1,51,'2024-01-01 07:43:00.141526','2024-01-01 07:43:00.141526',NULL,NULL),(18,'Pd7icOpNZMAWkpepM3VHbY2FLE1Bwe','2024-01-01 18:44:17.348300','read write',1,51,'2024-01-01 08:44:17.349692','2024-01-01 08:44:17.349692',NULL,NULL),(19,'4ZU5jVw0w2caGTuf4UJCaKA6QBt9ZB','2024-01-01 21:32:24.181954','read write',1,51,'2024-01-01 11:32:24.181954','2024-01-01 11:32:24.181954',NULL,NULL);
/*!40000 ALTER TABLE `oauth2_provider_accesstoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_provider_application`
--

DROP TABLE IF EXISTS `oauth2_provider_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `redirect_uris` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `authorization_grant_type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_secret` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `algorithm` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_logout_redirect_uris` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`),
  KEY `oauth2_provider_application_user_id_79829054_fk_ASSSs_user_id` (`user_id`),
  KEY `oauth2_provider_application_client_secret_53133678` (`client_secret`),
  CONSTRAINT `oauth2_provider_application_user_id_79829054_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_application`
--

LOCK TABLES `oauth2_provider_application` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_application` DISABLE KEYS */;
INSERT INTO `oauth2_provider_application` VALUES (1,'cN1kSkRY92F0i41vOzIeNrtRHhHK3axzq5rOS6yA','','confidential','password','pbkdf2_sha256$600000$Xwo9bR5bzbl6JNG7blrgcP$2kGSrfmvrEB3vgGmXuvK5+8EgPTraTODsPmJOWRiORU=','ASSS',56,0,'2023-12-26 15:14:48.608752','2023-12-26 15:14:48.608752','','');
/*!40000 ALTER TABLE `oauth2_provider_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_provider_grant`
--

DROP TABLE IF EXISTS `oauth2_provider_grant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_grant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `redirect_uri` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `scope` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `code_challenge` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_challenge_method` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nonce` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `claims` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_grant_user_id_e8f62af8_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_grant_user_id_e8f62af8_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_grant`
--

LOCK TABLES `oauth2_provider_grant` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_grant` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_grant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_provider_idtoken`
--

DROP TABLE IF EXISTS `oauth2_provider_idtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_idtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jti` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jti` (`jti`),
  KEY `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_idtoken_user_id_dd512b59_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_idtoken_user_id_dd512b59_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_idtoken`
--

LOCK TABLES `oauth2_provider_idtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_idtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_idtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_provider_refreshtoken`
--

DROP TABLE IF EXISTS `oauth2_provider_refreshtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_refreshtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `access_token_id` bigint DEFAULT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `revoked` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token_id` (`access_token_id`),
  UNIQUE KEY `oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq` (`token`,`revoked`),
  KEY `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_refreshtoken_user_id_da837fce_fk_ASSSs_user_id` (`user_id`),
  CONSTRAINT `oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_provider_accesstoken` (`id`),
  CONSTRAINT `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_refreshtoken_user_id_da837fce_fk_ASSSs_user_id` FOREIGN KEY (`user_id`) REFERENCES `assss_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_refreshtoken`
--

LOCK TABLES `oauth2_provider_refreshtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_refreshtoken` DISABLE KEYS */;
INSERT INTO `oauth2_provider_refreshtoken` VALUES (1,'mAC25rvxg23GcoDLItvFLkIAdGCjVK',1,1,49,'2023-12-26 15:33:37.101977','2023-12-26 15:33:37.101977',NULL),(2,'8yZriF5mAwP3c2NwMfA89hUKZjl4uN',2,1,49,'2023-12-26 16:44:15.024453','2023-12-26 16:44:15.024453',NULL),(3,'pgvk8OhbvBthtmKtbqwI0J0Uq9gJMV',3,1,49,'2023-12-27 06:18:14.244403','2023-12-27 06:18:14.244403',NULL),(4,'pvUVDstJqLLRwWkTg1fUyBhMfxGiIm',4,1,49,'2023-12-27 06:23:24.938386','2023-12-27 06:23:24.938386',NULL),(5,'m3sn4GKXzybkEvqCb7sofukTG32hl5',5,1,49,'2023-12-27 06:36:33.674856','2023-12-27 06:36:33.674856',NULL),(6,'1o9YisS4YRznaJG88mfJ2cpvJp0gAn',6,1,50,'2023-12-27 09:04:48.207993','2023-12-27 09:04:48.208992',NULL),(7,'DyAvWV4iwYfw5d0pkxow5XqSZiFWw6',7,1,50,'2023-12-27 09:57:02.409629','2023-12-27 09:57:02.409629',NULL),(8,'jGG4QrGOU6TiNXtYO7s8ssceyOcUqX',8,1,50,'2023-12-27 12:16:22.136132','2023-12-27 12:16:22.136132',NULL),(9,'V5MsnIdOlpXVAV2Tmj4pPiHjx3ZJKQ',9,1,50,'2023-12-28 07:01:53.066524','2023-12-28 07:01:53.066524',NULL),(10,'fvSgjxfNGcQhVLs5Sj0MsHPQwlp4Sq',10,1,51,'2023-12-28 07:46:14.084130','2023-12-28 07:46:14.084130',NULL),(11,'V4hvbyfwM6E3qyC9luiJbKKkVGcfH5',11,1,54,'2023-12-28 07:47:46.224380','2023-12-28 07:47:46.224380',NULL),(12,'iqAQDm58SulszlMlC7Wsduo03I4kRZ',12,1,51,'2023-12-28 08:55:50.701552','2023-12-28 08:55:50.701552',NULL),(13,'QIV456RFJGWfwN2KAVLRaHRdKFKpO7',13,1,50,'2023-12-28 09:13:21.821556','2023-12-28 09:13:21.821556',NULL),(14,'OK6oYGxy35LoJt0OMAG147f7hzbTMM',14,1,51,'2023-12-28 10:10:12.408825','2023-12-28 10:10:12.408825',NULL),(15,'VBHpkaQ9ft8NxeP3cLFslkcjRrz6ou',15,1,51,'2023-12-31 05:39:04.840005','2023-12-31 05:39:04.840005',NULL),(16,'NLr8ypCkW7mgnyEHTKzYQcFlbPFjdS',16,1,51,'2023-12-31 06:33:37.032686','2023-12-31 06:33:37.032686',NULL),(17,'iNJmZbbVeVgum0ciqOn5mmahqrpKAa',17,1,51,'2024-01-01 07:43:00.208915','2024-01-01 07:43:00.208915',NULL),(18,'b9bwBpDf1sbUANFeIMQ6sl67Zb7mkw',18,1,51,'2024-01-01 08:44:17.383148','2024-01-01 08:44:17.383148',NULL),(19,'bzdibMYHoFXTgxUt4jH0wmPxEZVi6A',19,1,51,'2024-01-01 11:32:24.238018','2024-01-01 11:32:24.238018',NULL);
/*!40000 ALTER TABLE `oauth2_provider_refreshtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-01 18:35:05
