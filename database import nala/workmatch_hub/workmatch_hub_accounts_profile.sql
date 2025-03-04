-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: workmatch_hub
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `immediate_notifications` tinyint(1) NOT NULL,
  `daily_notifications` tinyint(1) NOT NULL,
  `weekly_notifications` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  `availability` varchar(255) DEFAULT NULL,
  `company_description` longtext,
  `company_logo` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `contact_person` varchar(255) DEFAULT NULL,
  `education` longtext,
  `employer_name` varchar(255) DEFAULT NULL,
  `experience` longtext,
  `facebook_link` varchar(200) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `is_small_scale` tinyint(1) NOT NULL,
  `job_preferences` longtext,
  `location` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `resume` varchar(100) DEFAULT NULL,
  `skills` longtext,
  `website` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,0,0,0,1,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,'','',NULL,NULL),(2,0,1,0,2,'everyday',NULL,'','0987654321',NULL,'asd',NULL,'asd','https://www.facebook.com/HeiHeiPH/','Heihei',NULL,0,'asd',NULL,'profile_pictures/heihei_a8AMNVk.jpg','resumes/hahaha_nWM4Ckt.jpg','asd',NULL),(3,0,1,0,3,NULL,'AMD is the high performance and adaptive computing leader, powering the products and services that help solve the world’s most important challenges. Our technologies advance the future of the data center, embedded, gaming and PC markets.\r\n\r\nFounded in 1969 as a Silicon Valley start-up, the AMD journey began with dozens of employees who were passionate about creating leading-edge semiconductor products. AMD has grown into a global company setting the standard for modern computing, with many important industry firsts and major technological achievements along the way.','company_logos/amd.jpg','0987654321','Heihei',NULL,'AMD',NULL,'https://www.facebook.com/AMD.Philippines/?brand_redir=23542086472',NULL,'Semiconductors, Computer hardware, Autonomous cars, Automation, Artificial intelligence',0,NULL,NULL,'','',NULL,'https://www.amd.com/en/corporate.html');
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-02  9:18:15
