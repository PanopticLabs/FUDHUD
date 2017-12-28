-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 28, 2017 at 08:52 AM
-- Server version: 5.7.20-0ubuntu0.17.10.1
-- PHP Version: 7.1.11-0ubuntu0.17.10.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `panoptic_twitter`
--

-- --------------------------------------------------------

--
-- Table structure for table `crypto_graph`
--

CREATE TABLE `crypto_graph` (
  `connectionID` int(20) UNSIGNED NOT NULL,
  `userID` int(10) UNSIGNED NOT NULL,
  `followerID` int(10) UNSIGNED NOT NULL,
  `followers` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_mentions`
--

CREATE TABLE `crypto_mentions` (
  `mentionID` int(10) UNSIGNED NOT NULL,
  `date` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) UNSIGNED NOT NULL,
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_users`
--

CREATE TABLE `crypto_users` (
  `userID` int(10) UNSIGNED NOT NULL,
  `twitterID` varchar(20) CHARACTER SET utf8 NOT NULL,
  `name` varchar(140) CHARACTER SET utf8 NOT NULL,
  `screenName` varchar(140) CHARACTER SET utf8 NOT NULL,
  `description` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(140) CHARACTER SET utf8 DEFAULT NULL,
  `timezone` varchar(140) CHARACTER SET utf8 DEFAULT NULL,
  `followers` int(10) UNSIGNED NOT NULL,
  `friends` int(10) UNSIGNED NOT NULL,
  `indexed` int(1) UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `spammers`
--

CREATE TABLE `spammers` (
  `twitterID` varchar(30) NOT NULL,
  `name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crypto_graph`
--
ALTER TABLE `crypto_graph`
  ADD PRIMARY KEY (`connectionID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `followerID` (`followerID`),
  ADD KEY `followers` (`followers`);

--
-- Indexes for table `crypto_mentions`
--
ALTER TABLE `crypto_mentions`
  ADD PRIMARY KEY (`mentionID`),
  ADD KEY `topic` (`topic`),
  ADD KEY `mentions` (`mentions`),
  ADD KEY `sentiment` (`sentiment`);

--
-- Indexes for table `crypto_users`
--
ALTER TABLE `crypto_users`
  ADD PRIMARY KEY (`userID`),
  ADD KEY `indexed` (`indexed`),
  ADD KEY `timezone` (`timezone`);

--
-- Indexes for table `spammers`
--
ALTER TABLE `spammers`
  ADD PRIMARY KEY (`twitterID`),
  ADD KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crypto_graph`
--
ALTER TABLE `crypto_graph`
  MODIFY `connectionID` int(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `crypto_mentions`
--
ALTER TABLE `crypto_mentions`
  MODIFY `mentionID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9039;
--
-- AUTO_INCREMENT for table `crypto_users`
--
ALTER TABLE `crypto_users`
  MODIFY `userID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24996;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
