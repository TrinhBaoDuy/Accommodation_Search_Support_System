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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_booking`
--

LOCK TABLES `assss_booking` WRITE;
/*!40000 ALTER TABLE `assss_booking` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_comment`
--

LOCK TABLES `assss_comment` WRITE;
/*!40000 ALTER TABLE `assss_comment` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_discount`
--

LOCK TABLES `assss_discount` WRITE;
/*!40000 ALTER TABLE `assss_discount` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_follow`
--

LOCK TABLES `assss_follow` WRITE;
/*!40000 ALTER TABLE `assss_follow` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_house`
--

LOCK TABLES `assss_house` WRITE;
/*!40000 ALTER TABLE `assss_house` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_image`
--

LOCK TABLES `assss_image` WRITE;
/*!40000 ALTER TABLE `assss_image` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_post`
--

LOCK TABLES `assss_post` WRITE;
/*!40000 ALTER TABLE `assss_post` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_postingprice`
--

LOCK TABLES `assss_postingprice` WRITE;
/*!40000 ALTER TABLE `assss_postingprice` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_role`
--

LOCK TABLES `assss_role` WRITE;
/*!40000 ALTER TABLE `assss_role` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assss_user`
--

LOCK TABLES `assss_user` WRITE;
/*!40000 ALTER TABLE `assss_user` DISABLE KEYS */;
INSERT INTO `assss_user` VALUES (1,'pbkdf2_sha256$720000$3CaCLL4loPyAGyeGx4fxwm$pkW07H45GnDC5knI9t0PK/QTQAyUz2JZmq+LKaK+MQo=','2024-01-02 04:58:23.221300',1,'admin','','','admin@gmail.com',1,1,'2024-01-02 04:57:39.801446',NULL,NULL,NULL,0,NULL,1,'2024-01-02','2024-01-02',NULL,NULL);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-01-02 04:56:39.197801'),(2,'contenttypes','0002_remove_content_type_name','2024-01-02 04:56:39.274594'),(3,'auth','0001_initial','2024-01-02 04:56:39.526503'),(4,'auth','0002_alter_permission_name_max_length','2024-01-02 04:56:39.579454'),(5,'auth','0003_alter_user_email_max_length','2024-01-02 04:56:39.587635'),(6,'auth','0004_alter_user_username_opts','2024-01-02 04:56:39.596934'),(7,'auth','0005_alter_user_last_login_null','2024-01-02 04:56:39.605177'),(8,'auth','0006_require_contenttypes_0002','2024-01-02 04:56:39.607868'),(9,'auth','0007_alter_validators_add_error_messages','2024-01-02 04:56:39.615845'),(10,'auth','0008_alter_user_username_max_length','2024-01-02 04:56:39.622638'),(11,'auth','0009_alter_user_last_name_max_length','2024-01-02 04:56:39.627509'),(12,'auth','0010_alter_group_name_max_length','2024-01-02 04:56:39.643071'),(13,'auth','0011_update_proxy_permissions','2024-01-02 04:56:39.649518'),(14,'auth','0012_alter_user_first_name_max_length','2024-01-02 04:56:39.656881'),(15,'ASSSs','0001_initial','2024-01-02 04:56:39.983662'),(16,'ASSSs','0002_house_acreage_house_price_house_quantity','2024-01-02 04:56:40.032976'),(17,'ASSSs','0003_discount_postingprice_role_user_address_user_avatar_and_more','2024-01-02 04:56:41.198903'),(18,'ASSSs','0004_alter_user_avatar','2024-01-02 04:56:41.319108'),(19,'ASSSs','0005_alter_image_imageurl','2024-01-02 04:56:41.393713'),(20,'ASSSs','0006_alter_image_imageurl_alter_user_avatar','2024-01-02 04:56:41.522287'),(21,'ASSSs','0007_alter_booking_options_alter_comment_options_and_more','2024-01-02 04:56:42.611940'),(22,'ASSSs','0008_booking_deleted_date_comment_deleted_date_and_more','2024-01-02 04:56:42.848556'),(23,'ASSSs','0009_alter_user_avatar','2024-01-02 04:56:42.892913'),(24,'ASSSs','0010_alter_user_avatar','2024-01-02 04:56:42.977050'),(25,'ASSSs','0011_alter_user_avatar','2024-01-02 04:56:43.021895'),(26,'ASSSs','0012_alter_user_avatar','2024-01-02 04:56:43.103671'),(27,'ASSSs','0013_alter_image_imageurl','2024-01-02 04:56:43.153701'),(28,'ASSSs','0014_user_gender','2024-01-02 04:56:43.199829'),(29,'admin','0001_initial','2024-01-02 04:56:43.348888'),(30,'admin','0002_logentry_remove_auto_add','2024-01-02 04:56:43.366729'),(31,'admin','0003_logentry_add_action_flag_choices','2024-01-02 04:56:43.379625'),(32,'oauth2_provider','0001_initial','2024-01-02 04:56:44.165475'),(33,'oauth2_provider','0002_auto_20190406_1805','2024-01-02 04:56:44.256964'),(34,'oauth2_provider','0003_auto_20201211_1314','2024-01-02 04:56:44.335247'),(35,'oauth2_provider','0004_auto_20200902_2022','2024-01-02 04:56:44.809186'),(36,'oauth2_provider','0005_auto_20211222_2352','2024-01-02 04:56:44.994613'),(37,'oauth2_provider','0006_alter_application_client_secret','2024-01-02 04:56:45.037091'),(38,'oauth2_provider','0007_application_post_logout_redirect_uris','2024-01-02 04:56:45.116407'),(39,'sessions','0001_initial','2024-01-02 04:56:45.153979');
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
INSERT INTO `django_session` VALUES ('o59jqwua8klyun0ccjlpn9k58gyui9fk','.eJxVjEEOwiAQRe_C2hAGOrS4dO8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3EWIE6_W6D44LqDdKd6azK2ui5zkLsiD9rltSV-Xg7376BQL99aJUbUTgPaTMgchwxWj2gn5ZQxGa2LA2dKBiZA0ClGF2wGYOVGRUq8P8sUNz0:1rKWr9:A50koJAsJdx7lqa49ok9tEpkXWI0Rxzt2LxI7BbXp5c','2024-01-16 04:58:23.330675');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_accesstoken`
--

LOCK TABLES `oauth2_provider_accesstoken` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_accesstoken` DISABLE KEYS */;
INSERT INTO `oauth2_provider_accesstoken` VALUES (1,'icPJkZlH8jo78KBhKwsBvDfuwTO4Fq','2024-01-02 15:00:14.137171','read write',1,1,'2024-01-02 05:00:14.138176','2024-01-02 05:00:14.138176',NULL,NULL),(2,'fDd7PYN9nKXYbhyff3ICEbQKfJzPOC','2024-01-02 15:02:36.655573','read write',1,1,'2024-01-02 05:02:36.655573','2024-01-02 05:02:36.655573',NULL,NULL);
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
INSERT INTO `oauth2_provider_application` VALUES (1,'UXTi69lodcxqmENTZITNy3e0EHIJ64UzUqnb9Hu4','','confidential','password','pbkdf2_sha256$720000$5d4IEEcSQB4HNCSFLy3pq8$E6S/CKRouUaQ2kGzSZegTtEbkNOw1Qe+NiBBGd8Dy1o=','App',1,0,'2024-01-02 04:59:41.788041','2024-01-02 04:59:41.788041','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_refreshtoken`
--

LOCK TABLES `oauth2_provider_refreshtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_provider_refreshtoken` DISABLE KEYS */;
INSERT INTO `oauth2_provider_refreshtoken` VALUES (1,'SjiewMNl9jOeHSnR0Wg2l3fFJHmIUB',1,1,1,'2024-01-02 05:00:14.172646','2024-01-02 05:00:14.172646',NULL),(2,'mUzz5phnz2rncXjNaN2iCM889zVMiZ',2,1,1,'2024-01-02 05:02:36.657547','2024-01-02 05:02:36.657547',NULL);
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

-- Dump completed on 2024-01-02 12:07:06
