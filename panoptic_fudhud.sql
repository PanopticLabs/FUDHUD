-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: panoptic_fudhud
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coins`
--

DROP TABLE IF EXISTS `coins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coins` (
  `coinID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cryptocompareID` int(10) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `imageURL` varchar(500) NOT NULL,
  `twitterURL` varchar(500) NOT NULL,
  `redditURL` varchar(500) NOT NULL,
  `facebookURL` varchar(500) NOT NULL,
  `gitURL` varchar(500) NOT NULL,
  PRIMARY KEY (`coinID`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `symbol` (`symbol`),
  UNIQUE KEY `cryptocompareID` (`cryptocompareID`),
  KEY `imageURL` (`imageURL`) USING BTREE,
  KEY `twitterURL` (`twitterURL`) USING BTREE,
  KEY `redditURL` (`redditURL`) USING BTREE,
  KEY `facebookURL` (`facebookURL`) USING BTREE,
  KEY `gitURL` (`gitURL`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `priceStats`
--

DROP TABLE IF EXISTS `priceStats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `priceStats` (
  `priceStatID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `coinID` int(10) unsigned NOT NULL,
  `datetime` datetime NOT NULL,
  `usd` double(20,10) unsigned NOT NULL,
  `btc` double(20,10) unsigned NOT NULL,
  `marketcap` double(20,2) unsigned NOT NULL,
  `dailyVolume` double(20,2) unsigned NOT NULL,
  `hourlyChange` double(20,10) NOT NULL,
  `dailyChange` double(20,10) NOT NULL,
  `weeklyChange` double(20,10) NOT NULL,
  `lastUpdate` int(20) unsigned NOT NULL,
  PRIMARY KEY (`priceStatID`),
  KEY `coinID` (`coinID`),
  KEY `datetime` (`datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=387 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_activity`
--

DROP TABLE IF EXISTS `reddit_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_activity` (
  `activityID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `subredditID` int(10) unsigned NOT NULL,
  `datetime` datetime NOT NULL,
  `subscribers` int(10) unsigned NOT NULL DEFAULT '0',
  `activeAccounts` int(10) unsigned NOT NULL DEFAULT '0',
  `newPosts` int(10) unsigned NOT NULL DEFAULT '0',
  `frontpageSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`activityID`),
  KEY `datetime` (`datetime`),
  KEY `subscribers` (`subscribers`),
  KEY `activeAccounts` (`activeAccounts`),
  KEY `newPosts` (`newPosts`),
  KEY `subredditID` (`subredditID`),
  KEY `frontpageSentiment` (`frontpageSentiment`)
) ENGINE=InnoDB AUTO_INCREMENT=424652 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_comments`
--

DROP TABLE IF EXISTS `reddit_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_comments` (
  `commentID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `commentUnique` varchar(10) NOT NULL,
  `postUnique` varchar(16) NOT NULL DEFAULT '',
  `parentUnique` varchar(16) NOT NULL DEFAULT '',
  `userID` int(10) unsigned NOT NULL,
  `unix` int(16) unsigned NOT NULL,
  `body` varchar(5000) NOT NULL DEFAULT '',
  `score` int(10) NOT NULL DEFAULT '0',
  `ups` int(10) NOT NULL DEFAULT '0',
  `downs` int(10) NOT NULL DEFAULT '0',
  `controversiality` int(3) unsigned NOT NULL DEFAULT '0',
  `depth` int(3) unsigned NOT NULL DEFAULT '0',
  `sentiment` decimal(5,4) NOT NULL,
  PRIMARY KEY (`commentID`),
  UNIQUE KEY `commentUnique` (`commentUnique`),
  KEY `sentiment` (`sentiment`),
  KEY `downs` (`downs`),
  KEY `ups` (`ups`),
  KEY `score` (`score`),
  KEY `unix` (`unix`),
  KEY `postUnique` (`postUnique`),
  KEY `parentUnique` (`parentUnique`)
) ENGINE=InnoDB AUTO_INCREMENT=927884 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_mentions`
--

DROP TABLE IF EXISTS `reddit_mentions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_mentions` (
  `mentionID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) unsigned NOT NULL,
  `sentiment` decimal(5,4) NOT NULL,
  PRIMARY KEY (`mentionID`),
  KEY `mentions` (`mentions`),
  KEY `topic` (`topic`),
  KEY `datetime` (`date`),
  KEY `sentiment` (`sentiment`)
) ENGINE=InnoDB AUTO_INCREMENT=804565 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_posts`
--

DROP TABLE IF EXISTS `reddit_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_posts` (
  `postID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `postUnique` varchar(10) NOT NULL,
  `subredditID` int(10) unsigned NOT NULL,
  `userID` int(10) unsigned NOT NULL,
  `unix` int(16) unsigned NOT NULL,
  `title` varchar(1000) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `comments` int(6) unsigned NOT NULL DEFAULT '0',
  `score` int(10) NOT NULL DEFAULT '0',
  `ups` int(10) NOT NULL DEFAULT '0',
  `downs` int(10) NOT NULL DEFAULT '0',
  `crossposts` int(3) unsigned NOT NULL DEFAULT '0',
  `postSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000',
  `commentSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`postID`),
  UNIQUE KEY `postUnique` (`postUnique`),
  KEY `postSentiment` (`postSentiment`),
  KEY `downs` (`downs`),
  KEY `ups` (`ups`),
  KEY `score` (`score`),
  KEY `commentSentiment` (`commentSentiment`),
  KEY `author` (`userID`),
  KEY `crossposts` (`crossposts`),
  KEY `subredditID` (`subredditID`)
) ENGINE=InnoDB AUTO_INCREMENT=267725 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_subreddits`
--

DROP TABLE IF EXISTS `reddit_subreddits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_subreddits` (
  `subredditID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(128) NOT NULL,
  `topic` varchar(32) NOT NULL,
  PRIMARY KEY (`subredditID`),
  KEY `name` (`name`),
  KEY `topic` (`topic`)
) ENGINE=InnoDB AUTO_INCREMENT=362 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reddit_users`
--

DROP TABLE IF EXISTS `reddit_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reddit_users` (
  `userID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `comments` int(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`userID`),
  KEY `comments` (`comments`)
) ENGINE=InnoDB AUTO_INCREMENT=161003 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialStats`
--

DROP TABLE IF EXISTS `socialStats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialStats` (
  `socialStatID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `coinID` int(10) unsigned NOT NULL,
  `datetime` datetime NOT NULL,
  `twitter_followers` int(10) unsigned NOT NULL,
  `twitter_following` int(10) unsigned NOT NULL,
  `twitter_statuses` int(10) unsigned NOT NULL,
  `twitter_points` int(10) unsigned NOT NULL,
  `reddit_subscribers` int(10) unsigned NOT NULL,
  `reddit_activeUsers` int(10) unsigned NOT NULL,
  `reddit_hourlyPosts` double(20,10) unsigned NOT NULL,
  `reddit_dailyPosts` double(20,10) unsigned NOT NULL,
  `reddit_hourlyComments` double(20,10) unsigned NOT NULL,
  `reddit_dailyComments` double(20,10) unsigned NOT NULL,
  `reddit_points` int(10) unsigned NOT NULL,
  `facebook_likes` int(10) unsigned NOT NULL,
  `facebook_talking` int(10) unsigned NOT NULL,
  `facebook_points` int(10) unsigned NOT NULL,
  `git_stars` int(10) unsigned NOT NULL,
  `git_forks` int(10) unsigned NOT NULL,
  `git_subscribers` int(10) unsigned NOT NULL,
  `git_size` int(10) unsigned NOT NULL,
  `git_lastUpdate` int(10) unsigned NOT NULL,
  `git_lastPush` int(10) unsigned NOT NULL,
  `git_openIssues` int(10) unsigned NOT NULL,
  `git_closedIssues` int(10) unsigned NOT NULL,
  `git_openPullIssues` int(10) unsigned NOT NULL,
  `git_closedPullIssues` int(10) unsigned NOT NULL,
  PRIMARY KEY (`socialStatID`),
  KEY `datetime` (`datetime`),
  KEY `coinID` (`coinID`)
) ENGINE=InnoDB AUTO_INCREMENT=389 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `twitter_mentions`
--

DROP TABLE IF EXISTS `twitter_mentions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `twitter_mentions` (
  `mentionID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) unsigned NOT NULL,
  `sentiment` decimal(5,4) NOT NULL,
  PRIMARY KEY (`mentionID`),
  KEY `topic` (`topic`),
  KEY `mentions` (`mentions`),
  KEY `sentiment` (`sentiment`)
) ENGINE=InnoDB AUTO_INCREMENT=936668 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `twitter_spammers`
--

DROP TABLE IF EXISTS `twitter_spammers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `twitter_spammers` (
  `twitterID` varchar(30) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`twitterID`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `twitter_users`
--

DROP TABLE IF EXISTS `twitter_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `twitter_users` (
  `userID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `twitterID` varchar(20) CHARACTER SET utf8 NOT NULL,
  `name` varchar(140) CHARACTER SET utf8 NOT NULL,
  `screenName` varchar(140) CHARACTER SET utf8 NOT NULL,
  `description` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(140) CHARACTER SET utf8 DEFAULT NULL,
  `timezone` varchar(140) CHARACTER SET utf8 DEFAULT NULL,
  `followers` int(10) unsigned NOT NULL,
  `friends` int(10) unsigned NOT NULL,
  `indexed` int(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`userID`),
  KEY `indexed` (`indexed`),
  KEY `timezone` (`timezone`)
) ENGINE=InnoDB AUTO_INCREMENT=375517 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-10 20:17:50
