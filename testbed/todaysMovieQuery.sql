CREATE DATABASE  IF NOT EXISTS `todays_movie` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `todays_movie`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: todays_movie
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie` (
  `MOVIE_SEQ` int NOT NULL AUTO_INCREMENT,
  `SUBJECT` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `COUNTRY` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `GENRE` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `DIRECTOR` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `SUMMARY` longtext,
  `GRADE` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`MOVIE_SEQ`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `movie_play`
--

DROP TABLE IF EXISTS `movie_play`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie_play` (
  `PLAY_SEQ` int NOT NULL AUTO_INCREMENT,
  `MOVIE_SEQ` int NOT NULL,
  `THEATERS_SEQ` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `START_TIME` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `RUNNING_TIME` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `SEATS` int DEFAULT NULL,
  `SEATS_LEFT` int DEFAULT NULL,
  `REGIST_DATE` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PLAY_SEQ`),
  KEY `MOVIE_SEQ` (`MOVIE_SEQ`),
  KEY `THEATERS_SEQ` (`THEATERS_SEQ`),
  CONSTRAINT `movie_play_ibfk_1` FOREIGN KEY (`MOVIE_SEQ`) REFERENCES `movie` (`MOVIE_SEQ`),
  CONSTRAINT `movie_play_ibfk_2` FOREIGN KEY (`THEATERS_SEQ`) REFERENCES `theaters` (`THEATERS_SEQ`)
) ENGINE=InnoDB AUTO_INCREMENT=3825 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_play`
--

--
-- Table structure for table `theaters`
--

DROP TABLE IF EXISTS `theaters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `theaters` (
  `SEQ` int NOT NULL AUTO_INCREMENT,
  `THEATERS` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `THEATERS_SEQ` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TH_NAME` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `LOCATION` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`SEQ`),
  KEY `MOVIE_PLAY` (`THEATERS_SEQ`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `theaters`
--

LOCK TABLES `theaters` WRITE;
/*!40000 ALTER TABLE `theaters` DISABLE KEYS */;
INSERT INTO `theaters` VALUES (1,'CGV','C-0056','강남',NULL),(2,'CGV','C-0001','강변',NULL),(3,'CGV','C-0229','건대입구',NULL),(4,'CGV','C-0010','구로',NULL),(5,'CGV','C-0063','대학로',NULL),(6,'CGV','C-0252','동대문',NULL),(7,'CGV','C-0230','등촌',NULL),(8,'CGV','C-0009','명동',NULL),(9,'CGV','C-0105','명동역 씨네라이브러리',NULL),(10,'CGV','C-0011','목동',NULL),(11,'CGV','C-0057','미아',NULL),(12,'CGV','C-0030','불광',NULL),(13,'CGV','C-0046','상봉',NULL),(14,'CGV','C-0300','성신여대입구',NULL),(15,'CGV','C-0088','송파',NULL),(16,'CGV','C-0276','수유',NULL),(17,'CGV','C-0150','신촌아트레온',NULL),(18,'CGV','C-0040','압구정',NULL),(19,'CGV','C-0112','여의도',NULL),(20,'CGV','C-0059','영등포',NULL),(21,'CGV','C-0074','왕십리',NULL),(22,'CGV','C-0013','용산아이파크몰',NULL),(23,'CGV','C-0131','중계',NULL),(24,'CGV','C-0199','천호',NULL),(25,'CGV','C-0107','청담씨네시티',NULL),(26,'CGV','C-0223','피카디리1958',NULL),(27,'CGV','C-0164','하계',NULL),(28,'CGV','C-0191','홍대',NULL),(29,'CGV','C-P001','CINE de CHEF 압구정',NULL),(30,'CGV','C-P013','CINE de CHEF 용산아이파크몰',NULL),(31,'LOTTE','L-1013','가산디지털',NULL),(32,'LOTTE','L-1018','가양',NULL),(33,'LOTTE','L-9010','강동',NULL),(34,'LOTTE','L-1004','건대입구',NULL),(35,'LOTTE','L-1009','김포공항',NULL),(36,'LOTTE','L-1003','노원',NULL),(37,'LOTTE','L-1017','독산',NULL),(38,'LOTTE','L-9056','브로드웨이(신사)',NULL),(39,'LOTTE','L-1012','서울대입구',NULL),(40,'LOTTE','L-1019','수락산',NULL),(41,'LOTTE','L-1022','수유',NULL),(42,'LOTTE','L-1015','신도림',NULL),(43,'LOTTE','L-1007','신림',NULL),(44,'LOTTE','L-1001','에비뉴엘(명동)',NULL),(45,'LOTTE','L-1002','영등포',NULL),(46,'LOTTE','L-1014','용산',NULL),(47,'LOTTE','L-1016','월드타워',NULL),(48,'LOTTE','L-1021','은평(롯데몰)',NULL),(49,'LOTTE','L-9053','장안',NULL),(50,'LOTTE','L-1008','청량리',NULL),(51,'LOTTE','L-1010','합정',NULL),(52,'LOTTE','L-1005','홍대입구',NULL),(53,'LOTTE','L-1011','황학',NULL),(54,'MEGABOX','M-1372','강남',NULL),(55,'MEGABOX','M-1359','강남대로(씨티)',NULL),(56,'MEGABOX','M-1341','강동',NULL),(57,'MEGABOX','M-1003','동대문',NULL),(58,'MEGABOX','M-1572','마곡',NULL),(59,'MEGABOX','M-1581','목동',NULL),(60,'MEGABOX','M-1311','상봉',NULL),(61,'MEGABOX','M-1211','상암월드컵경기장',NULL),(62,'MEGABOX','M-1331','성수',NULL),(63,'MEGABOX','M-1371','센트럴',NULL),(64,'MEGABOX','M-1381','송파파크하비오',NULL),(65,'MEGABOX','M-1202','신촌',NULL),(66,'MEGABOX','M-1221','은평',NULL),(67,'MEGABOX','M-1561','이수',NULL),(68,'MEGABOX','M-1321','창동',NULL),(69,'MEGABOX','M-1351','코엑스',NULL),(70,'MEGABOX','M-1212','홍대',NULL),(71,'MEGABOX','M-1571','화곡',NULL),(72,'MEGABOX','M-1562','ARTNINE',NULL);
/*!40000 ALTER TABLE `theaters` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-13 18:04:54
