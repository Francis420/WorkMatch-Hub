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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1ojgto2dew07zafi0k92ddxxcsmfqom5','.eJxVjMsOwiAQRf-FtSFAebp07zcQhhmkaiAp7cr479qkC93ec859sZi2tcZt0BJnZGem2Ol3g5Qf1HaA99Runefe1mUGviv8oINfO9Lzcrh_BzWN-q29QsjSyTIVLCYkcoQBzCQBvAKgDMIoUEIHLYNxthibBfqgYQJJ1rP3BwMwODc:1tNSqZ:EYhoZ6ucJnzpxNRtImHYoQhYDWqg_y-CVi370zf8KC0','2024-12-31 08:22:27.278044'),('85s5fxct9neatg5ja5fq476ix6e5y809','.eJxVjMsOwiAQRf-FtSENMDxcuvcbyDADUjWQlHZl_Hdt0oVu7znnvkTEba1xG3mJM4uz0OL0uyWkR2474Du2W5fU27rMSe6KPOiQ1875eTncv4OKo37rECblQZMvCMkpY22yho2fgsnFKQIKiC5k8KwBitOauEB26J0nw0W8P8wvN9U:1tTh3j:4dY0hUWxdr9b-sP2lCRlhO4xH46A0c5NuADeDoFBDtA','2025-01-17 12:45:47.022988'),('hwjaeqcgsopgigt6gcggez59iw97y8ss','.eJxVjMsOwiAQRf-FtSFAebp07zcQhhmkaiAp7cr479qkC93ec859sZi2tcZt0BJnZGem2Ol3g5Qf1HaA99Runefe1mUGviv8oINfO9Lzcrh_BzWN-q29QsjSyTIVLCYkcoQBzCQBvAKgDMIoUEIHLYNxthibBfqgYQJJ1rP3BwMwODc:1tO4Oh:8KZnwH5reqFMsaJnBBy_M19K2iiyHWd8o7XC6dtGbcw','2025-01-02 00:28:11.875104');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
