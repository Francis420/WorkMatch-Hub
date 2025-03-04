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
-- Table structure for table `jobs_jobpost`
--

DROP TABLE IF EXISTS `jobs_jobpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs_jobpost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `requirements` longtext NOT NULL,
  `location` varchar(255) NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `job_duration` varchar(255) DEFAULT NULL,
  `job_type` varchar(50) NOT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `employer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jobs_jobpost_employer_id_3098d2f7_fk_accounts_customuser_id` (`employer_id`),
  CONSTRAINT `jobs_jobpost_employer_id_3098d2f7_fk_accounts_customuser_id` FOREIGN KEY (`employer_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs_jobpost`
--

LOCK TABLES `jobs_jobpost` WRITE;
/*!40000 ALTER TABLE `jobs_jobpost` DISABLE KEYS */;
INSERT INTO `jobs_jobpost` VALUES (1,'Foreman','Help in construction','Knows the basic','Mars',5000.00,'2024-12-16 02:19:16.906503','5 times a week','contract',3000.00,3),(29,'Cook','Eats','fadas','Mars',214.00,'2024-12-17 03:28:37.839450','5 times a week','contract',234.00,3),(31,'Cook','heh','asdasd','Mars',1000.00,'2025-03-01 22:38:05.096672','5 times a week','one_time',1000.00,3),(32,'Cook','heh','asdasd','Mars',1000.00,'2025-03-01 22:40:54.582095','5 times a week','one_time',1000.00,3),(33,'Cook','heh','asdasd','Mars',1000.00,'2025-03-01 22:41:49.053651','5 times a week','one_time',1000.00,3),(34,'aaa','aaaa','aaa','mars',1212.00,'2025-03-01 22:52:04.092680','1212','contract',2121.00,3);
/*!40000 ALTER TABLE `jobs_jobpost` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-02  9:18:14
