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
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `verb` varchar(255) NOT NULL,
  `read` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `recipient_id` bigint NOT NULL,
  `target_id` bigint DEFAULT NULL,
  `sender_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_recipient_id_d055f3f0_fk_accounts_` (`recipient_id`),
  KEY `notifications_notification_target_id_1b4d0b9a_fk_jobs_jobpost_id` (`target_id`),
  KEY `notifications_notifi_sender_id_feea9ca3_fk_accounts_` (`sender_id`),
  CONSTRAINT `notifications_notifi_recipient_id_d055f3f0_fk_accounts_` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `notifications_notifi_sender_id_feea9ca3_fk_accounts_` FOREIGN KEY (`sender_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `notifications_notification_target_id_1b4d0b9a_fk_jobs_jobpost_id` FOREIGN KEY (`target_id`) REFERENCES `jobs_jobpost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
INSERT INTO `notifications_notification` VALUES (7,'admin1 has applied for your job posting: Foreman',1,'2024-12-16 09:06:40.905957',3,1,2),(8,'admin1 has applied for your job posting: Foreman',1,'2024-12-16 09:07:57.734648',3,1,2),(15,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:09:26.511375',2,1,3),(25,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:12:39.546599',2,1,3),(36,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:14:36.159007',2,1,3),(48,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:19:02.472219',2,1,3),(61,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:22:36.351015',2,1,3),(75,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:27:32.098652',2,1,3),(90,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:29:08.167314',2,1,3),(106,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:31:32.724556',2,1,3),(123,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:37:31.622340',2,1,3),(141,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:45:15.654258',2,1,3),(160,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:50:01.011577',2,1,3),(180,'New job alert: Foreman in Mars (matched on: location)',1,'2024-12-17 02:59:26.091521',2,1,3),(204,'New job alert: Cook in Mars (matched on: title, description, location)',1,'2024-12-17 03:28:37.860053',2,29,3),(206,'admin1 has applied for your job posting: Foreman',1,'2024-12-17 08:14:11.970565',3,1,2),(207,'admin1 has applied for your job posting: Cook',1,'2024-12-18 00:52:36.332292',3,29,2),(208,'admin1 has cancelled their application(s) for your job posting: Foreman',1,'2025-01-03 03:49:03.201952',3,1,2),(209,'admin1 has applied for your job posting: Foreman',1,'2025-01-03 03:49:13.757117',3,1,2),(210,'admin1 has cancelled their application(s) for your job posting: Foreman',1,'2025-03-01 22:31:15.550055',3,1,2),(211,'admin1 has applied for your job posting: Foreman',1,'2025-03-01 22:31:19.935650',3,1,2),(212,'New job alert: Cook in Mars (matched on: title, location)',1,'2025-03-01 22:38:05.125576',2,31,3),(213,'New job alert: Cook in Mars (matched on: title, location)',1,'2025-03-01 22:40:54.605872',2,32,3),(214,'New job alert: Cook in Mars (matched on: title, location)',1,'2025-03-01 22:41:49.072394',2,33,3),(215,'New job alert: aaa in mars (matched on: location)',1,'2025-03-01 22:52:04.113327',2,34,3),(216,'admin1 has applied for your job posting: aaa',1,'2025-03-01 22:53:06.592792',3,34,2);
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-02  9:18:16
