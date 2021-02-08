-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: cvranking
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phno` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'test','test@test.com','123456789','test'),(3,'khemchand','khemchand5487@gmail.com','8684991012','12345'),(4,'Amit','amit@test.com','1234567890','123');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_accounts`
--

DROP TABLE IF EXISTS `admin_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_accounts`
--

LOCK TABLES `admin_accounts` WRITE;
/*!40000 ALTER TABLE `admin_accounts` DISABLE KEYS */;
INSERT INTO `admin_accounts` VALUES (1,'admin','admin@admin.com','admin');
/*!40000 ALTER TABLE `admin_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_details`
--

DROP TABLE IF EXISTS `job_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_details` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `job_title` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `location` varchar(500) NOT NULL,
  `exp_required` int NOT NULL,
  `min_salary` int NOT NULL,
  `max_salary` int NOT NULL,
  `skills` varchar(1000) NOT NULL,
  `job_description` varchar(10000) NOT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_details`
--

LOCK TABLES `job_details` WRITE;
/*!40000 ALTER TABLE `job_details` DISABLE KEYS */;
INSERT INTO `job_details` VALUES (5,'python developer','webstrot technology pvt. ltd.','los angeles califonia po, 455001',2,15000,25000,'ui designer, developer, seniorit company, design, call center','ui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call centerui designer, developer, seniorit company, design, call center'),(6,'test_title1','webstrot technology pvt. ltd.','los angeles califonia po, 455001',2,10000,25000,'accounting, management','experience in private equity accounting – management fee, preferred return, catch up, carry interest and irr calculations. \r\nquarterly and monthly activities for all general ledger accounts, including reconcililations, compiling, and analyzing partnership and direct/ co-investment financials and schedules\r\npreparation of capital call / distribution notices and preparations of capital statements and financial statements.\r\n\r\n\r\n\r\n');
/*!40000 ALTER TABLE `job_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `quiz_no` varchar(11) NOT NULL,
  `questions` varchar(10000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
INSERT INTO `quizzes` VALUES (6,5,'1','{\'What is Python?\': [\'Markup Language\', \'Programming Language\', \'Snake\', \'Rat\', \'Programming Language\'], \'What is Python @?\': [\'Markup Language\', \'Programming Language\', \'Snake\', \'Rat\', \'Programming Language\']}'),(8,5,'2','{\'What is Python @?\': [\'Markup Language\', \'Programming Language\', \'Snake\', \'Rat\', \'Programming Language\']}'),(9,6,'2','{\'What is Python @?\': [\'Markup Language\', \'Programming Language\', \'Snake\', \'Rat\', \'Programming Language\']}'),(10,6,'1','{\'What is Python?\': [\'Markup Language\', \'Programming Language\', \'Snake\', \'Rat\', \'Programming Language\']}');
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `quiz_id` int DEFAULT NULL,
  `score` varchar(255) DEFAULT NULL,
  `cv_name` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (2,3,6,'100, 100.0','8f916ee3-LT-CV-201608.docx'),(3,1,6,'100','c6a41a87-Resume---Rohini-Prakash.pdf');
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_result`
--

DROP TABLE IF EXISTS `user_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `message` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_result`
--

LOCK TABLES `user_result` WRITE;
/*!40000 ALTER TABLE `user_result` DISABLE KEYS */;
INSERT INTO `user_result` VALUES (2,3,'You are shortlisted for job id: 6'),(3,3,'You are shortlisted for job id: 6'),(4,3,'You are shortlisted for job id: 6'),(5,3,'You are shortlisted for job id: 6');
/*!40000 ALTER TABLE `user_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'cvranking'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-14 14:52:55
