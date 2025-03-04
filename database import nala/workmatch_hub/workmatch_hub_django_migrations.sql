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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-12-08 07:15:03.328748'),(2,'contenttypes','0002_remove_content_type_name','2024-12-08 07:15:03.455659'),(3,'auth','0001_initial','2024-12-08 07:15:03.833371'),(4,'auth','0002_alter_permission_name_max_length','2024-12-08 07:15:03.907200'),(5,'auth','0003_alter_user_email_max_length','2024-12-08 07:15:03.914456'),(6,'auth','0004_alter_user_username_opts','2024-12-08 07:15:03.924138'),(7,'auth','0005_alter_user_last_login_null','2024-12-08 07:15:03.932809'),(8,'auth','0006_require_contenttypes_0002','2024-12-08 07:15:03.936787'),(9,'auth','0007_alter_validators_add_error_messages','2024-12-08 07:15:03.944310'),(10,'auth','0008_alter_user_username_max_length','2024-12-08 07:15:03.951883'),(11,'auth','0009_alter_user_last_name_max_length','2024-12-08 07:15:03.959310'),(12,'auth','0010_alter_group_name_max_length','2024-12-08 07:15:03.979759'),(13,'auth','0011_update_proxy_permissions','2024-12-08 07:15:03.988372'),(14,'auth','0012_alter_user_first_name_max_length','2024-12-08 07:15:03.996675'),(15,'accounts','0001_initial','2024-12-08 07:15:04.771698'),(16,'accounts','0002_jobpost_budget_jobpost_job_duration_jobpost_job_type_and_more','2024-12-08 07:15:05.353568'),(17,'accounts','0003_alter_jobpost_job_type','2024-12-08 07:15:05.512323'),(18,'accounts','0004_remove_jobpost_employer_delete_jobalert_and_more','2024-12-08 07:15:05.626047'),(19,'admin','0001_initial','2024-12-08 07:15:05.795089'),(20,'admin','0002_logentry_remove_auto_add','2024-12-08 07:15:05.812744'),(21,'admin','0003_logentry_add_action_flag_choices','2024-12-08 07:15:05.828256'),(22,'jobs','0001_initial','2024-12-08 07:15:06.035698'),(23,'sessions','0001_initial','2024-12-08 07:15:06.089137'),(24,'accounts','0005_delete_feedback','2024-12-08 07:56:07.962462'),(25,'feedback','0001_initial','2024-12-08 07:56:08.238077'),(26,'accounts','0006_auditlog','2024-12-13 04:16:38.323794'),(27,'notifications','0001_initial','2024-12-16 06:55:59.374722'),(28,'jobs','0002_application','2024-12-16 07:22:40.204014'),(29,'notifications','0002_notification_sender','2024-12-16 08:49:44.561079'),(30,'jobs','0003_rename_industry_jobalert_job_description','2024-12-16 16:38:23.366677'),(31,'jobs','0004_remove_jobalert_created_at_jobalert_notified_jobs_and_more','2024-12-17 02:58:04.060545'),(32,'jobs','0005_jobalert_created_at_alter_jobalert_job_description_and_more','2024-12-17 02:58:04.342050'),(33,'jobs','0006_remove_application_applied_at_and_more','2024-12-18 00:46:49.517317');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
