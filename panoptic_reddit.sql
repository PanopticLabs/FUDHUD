-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 17, 2018 at 04:58 PM
-- Server version: 5.7.20-0ubuntu0.17.10.1
-- PHP Version: 7.1.11-0ubuntu0.17.10.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `panoptic_reddit`
--

-- --------------------------------------------------------

--
-- Table structure for table `crypto_activity`
--

CREATE TABLE `crypto_activity` (
  `activityID` int(10) UNSIGNED NOT NULL,
  `subredditID` int(10) UNSIGNED NOT NULL,
  `datetime` datetime NOT NULL,
  `subscribers` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `activeAccounts` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `newPosts` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `frontpageSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_comments`
--

CREATE TABLE `crypto_comments` (
  `commentID` int(10) UNSIGNED NOT NULL,
  `commentUnique` varchar(10) NOT NULL,
  `postUnique` varchar(16) NOT NULL DEFAULT '',
  `parentUnique` varchar(16) NOT NULL DEFAULT '',
  `userID` int(10) UNSIGNED NOT NULL,
  `unix` int(16) UNSIGNED NOT NULL,
  `body` varchar(5000) NOT NULL DEFAULT '',
  `score` int(10) NOT NULL DEFAULT '0',
  `ups` int(10) NOT NULL DEFAULT '0',
  `downs` int(10) NOT NULL DEFAULT '0',
  `controversiality` int(3) UNSIGNED NOT NULL DEFAULT '0',
  `depth` int(3) UNSIGNED NOT NULL DEFAULT '0',
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_mentions`
--

CREATE TABLE `crypto_mentions` (
  `mentionID` int(10) UNSIGNED NOT NULL,
  `datetime` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) UNSIGNED NOT NULL,
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_posts`
--

CREATE TABLE `crypto_posts` (
  `postID` int(10) UNSIGNED NOT NULL,
  `postUnique` varchar(10) NOT NULL,
  `subredditID` int(10) UNSIGNED NOT NULL,
  `userID` int(10) UNSIGNED NOT NULL,
  `unix` int(16) UNSIGNED NOT NULL,
  `title` varchar(1000) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `comments` int(6) UNSIGNED NOT NULL DEFAULT '0',
  `score` int(10) NOT NULL DEFAULT '0',
  `ups` int(10) NOT NULL DEFAULT '0',
  `downs` int(10) NOT NULL DEFAULT '0',
  `crossposts` int(3) UNSIGNED NOT NULL DEFAULT '0',
  `postSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000',
  `commentSentiment` decimal(5,4) NOT NULL DEFAULT '0.0000'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_subreddits`
--

CREATE TABLE `crypto_subreddits` (
  `subredditID` int(10) UNSIGNED NOT NULL,
  `name` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(128) NOT NULL,
  `topic` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `crypto_users`
--

CREATE TABLE `crypto_users` (
  `userID` int(10) UNSIGNED NOT NULL,
  `name` varchar(128) NOT NULL,
  `comments` int(5) UNSIGNED NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crypto_activity`
--
ALTER TABLE `crypto_activity`
  ADD PRIMARY KEY (`activityID`),
  ADD KEY `datetime` (`datetime`),
  ADD KEY `subscribers` (`subscribers`),
  ADD KEY `activeAccounts` (`activeAccounts`),
  ADD KEY `newPosts` (`newPosts`),
  ADD KEY `subredditID` (`subredditID`),
  ADD KEY `frontpageSentiment` (`frontpageSentiment`);

--
-- Indexes for table `crypto_comments`
--
ALTER TABLE `crypto_comments`
  ADD PRIMARY KEY (`commentID`),
  ADD UNIQUE KEY `commentUnique` (`commentUnique`),
  ADD KEY `sentiment` (`sentiment`),
  ADD KEY `downs` (`downs`),
  ADD KEY `ups` (`ups`),
  ADD KEY `score` (`score`),
  ADD KEY `unix` (`unix`),
  ADD KEY `postUnique` (`postUnique`),
  ADD KEY `parentUnique` (`parentUnique`);

--
-- Indexes for table `crypto_mentions`
--
ALTER TABLE `crypto_mentions`
  ADD PRIMARY KEY (`mentionID`),
  ADD KEY `mentions` (`mentions`),
  ADD KEY `topic` (`topic`),
  ADD KEY `datetime` (`datetime`),
  ADD KEY `sentiment` (`sentiment`);

--
-- Indexes for table `crypto_posts`
--
ALTER TABLE `crypto_posts`
  ADD PRIMARY KEY (`postID`),
  ADD UNIQUE KEY `postUnique` (`postUnique`),
  ADD KEY `postSentiment` (`postSentiment`),
  ADD KEY `downs` (`downs`),
  ADD KEY `ups` (`ups`),
  ADD KEY `score` (`score`),
  ADD KEY `commentSentiment` (`commentSentiment`),
  ADD KEY `author` (`userID`),
  ADD KEY `crossposts` (`crossposts`),
  ADD KEY `subredditID` (`subredditID`);

--
-- Indexes for table `crypto_subreddits`
--
ALTER TABLE `crypto_subreddits`
  ADD PRIMARY KEY (`subredditID`),
  ADD KEY `name` (`name`),
  ADD KEY `topic` (`topic`);

--
-- Indexes for table `crypto_users`
--
ALTER TABLE `crypto_users`
  ADD PRIMARY KEY (`userID`),
  ADD KEY `comments` (`comments`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crypto_activity`
--
ALTER TABLE `crypto_activity`
  MODIFY `activityID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=744;
--
-- AUTO_INCREMENT for table `crypto_comments`
--
ALTER TABLE `crypto_comments`
  MODIFY `commentID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46603;
--
-- AUTO_INCREMENT for table `crypto_mentions`
--
ALTER TABLE `crypto_mentions`
  MODIFY `mentionID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=765;
--
-- AUTO_INCREMENT for table `crypto_posts`
--
ALTER TABLE `crypto_posts`
  MODIFY `postID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14277;
--
-- AUTO_INCREMENT for table `crypto_subreddits`
--
ALTER TABLE `crypto_subreddits`
  MODIFY `subredditID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=172;
--
-- AUTO_INCREMENT for table `crypto_users`
--
ALTER TABLE `crypto_users`
  MODIFY `userID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26165;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
