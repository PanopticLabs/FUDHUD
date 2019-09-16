-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 10, 2019 at 01:16 PM
-- Server version: 5.7.27-0ubuntu0.18.04.1
-- PHP Version: 7.2.19-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `panoptic_fudhud`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth`
--

CREATE TABLE `auth` (
  `tokenID` int(8) UNSIGNED NOT NULL,
  `token` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `coins`
--

CREATE TABLE `coins` (
  `coinID` int(10) UNSIGNED NOT NULL,
  `cryptocompareID` int(10) UNSIGNED NOT NULL,
  `name` varchar(50) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `imageURL` varchar(500) NOT NULL,
  `twitterURL` varchar(500) NOT NULL,
  `redditURL` varchar(500) NOT NULL,
  `facebookURL` varchar(500) NOT NULL,
  `gitURL` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `priceStats`
--

CREATE TABLE `priceStats` (
  `priceStatID` int(10) UNSIGNED NOT NULL,
  `coinID` int(10) UNSIGNED NOT NULL,
  `datetime` datetime NOT NULL,
  `usd` double(20,10) UNSIGNED NOT NULL,
  `btc` double(20,10) UNSIGNED NOT NULL,
  `marketcap` double(20,2) UNSIGNED NOT NULL,
  `dailyVolume` double(20,2) UNSIGNED NOT NULL,
  `hourlyChange` double(20,10) NOT NULL,
  `dailyChange` double(20,10) NOT NULL,
  `weeklyChange` double(20,10) NOT NULL,
  `lastUpdate` int(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reddit_activity`
--

CREATE TABLE `reddit_activity` (
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
-- Table structure for table `reddit_comments`
--

CREATE TABLE `reddit_comments` (
  `commentID` int(10) UNSIGNED NOT NULL,
  `commentUnique` varchar(10) NOT NULL,
  `postUnique` varchar(16) NOT NULL DEFAULT '',
  `parentUnique` varchar(16) NOT NULL DEFAULT '',
  `userID` int(10) UNSIGNED NOT NULL,
  `unix` int(16) UNSIGNED NOT NULL,
  `body` varchar(10000) NOT NULL DEFAULT '',
  `score` int(10) NOT NULL DEFAULT '0',
  `ups` int(10) NOT NULL DEFAULT '0',
  `downs` int(10) NOT NULL DEFAULT '0',
  `controversiality` int(3) UNSIGNED NOT NULL DEFAULT '0',
  `depth` int(3) UNSIGNED NOT NULL DEFAULT '0',
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reddit_mentions`
--

CREATE TABLE `reddit_mentions` (
  `mentionID` int(10) UNSIGNED NOT NULL,
  `date` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) UNSIGNED NOT NULL,
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reddit_posts`
--

CREATE TABLE `reddit_posts` (
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
-- Table structure for table `reddit_subreddits`
--

CREATE TABLE `reddit_subreddits` (
  `subredditID` int(10) UNSIGNED NOT NULL,
  `name` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(128) NOT NULL,
  `topic` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reddit_users`
--

CREATE TABLE `reddit_users` (
  `userID` int(10) UNSIGNED NOT NULL,
  `name` varchar(128) NOT NULL,
  `comments` int(5) UNSIGNED NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `socialStats`
--

CREATE TABLE `socialStats` (
  `socialStatID` int(10) UNSIGNED NOT NULL,
  `coinID` int(10) UNSIGNED NOT NULL,
  `datetime` datetime NOT NULL,
  `twitter_followers` int(10) UNSIGNED NOT NULL,
  `twitter_following` int(10) UNSIGNED NOT NULL,
  `twitter_statuses` int(10) UNSIGNED NOT NULL,
  `twitter_points` int(10) UNSIGNED NOT NULL,
  `reddit_subscribers` int(10) UNSIGNED NOT NULL,
  `reddit_activeUsers` int(10) UNSIGNED NOT NULL,
  `reddit_hourlyPosts` double(20,10) UNSIGNED NOT NULL,
  `reddit_dailyPosts` double(20,10) UNSIGNED NOT NULL,
  `reddit_hourlyComments` double(20,10) UNSIGNED NOT NULL,
  `reddit_dailyComments` double(20,10) UNSIGNED NOT NULL,
  `reddit_points` int(10) UNSIGNED NOT NULL,
  `facebook_likes` int(10) UNSIGNED NOT NULL,
  `facebook_talking` int(10) UNSIGNED NOT NULL,
  `facebook_points` int(10) UNSIGNED NOT NULL,
  `git_stars` int(10) UNSIGNED NOT NULL,
  `git_forks` int(10) UNSIGNED NOT NULL,
  `git_subscribers` int(10) UNSIGNED NOT NULL,
  `git_size` int(10) UNSIGNED NOT NULL,
  `git_lastUpdate` int(10) UNSIGNED NOT NULL,
  `git_lastPush` int(10) UNSIGNED NOT NULL,
  `git_openIssues` int(10) UNSIGNED NOT NULL,
  `git_closedIssues` int(10) UNSIGNED NOT NULL,
  `git_openPullIssues` int(10) UNSIGNED NOT NULL,
  `git_closedPullIssues` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `twitter_mentions`
--

CREATE TABLE `twitter_mentions` (
  `mentionID` int(10) UNSIGNED NOT NULL,
  `date` datetime NOT NULL,
  `topic` varchar(64) NOT NULL,
  `mentions` int(5) UNSIGNED NOT NULL,
  `sentiment` decimal(5,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `twitter_spammers`
--

CREATE TABLE `twitter_spammers` (
  `twitterID` varchar(30) NOT NULL,
  `name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `twitter_users`
--

CREATE TABLE `twitter_users` (
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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth`
--
ALTER TABLE `auth`
  ADD PRIMARY KEY (`tokenID`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indexes for table `coins`
--
ALTER TABLE `coins`
  ADD PRIMARY KEY (`coinID`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `symbol` (`symbol`),
  ADD UNIQUE KEY `cryptocompareID` (`cryptocompareID`),
  ADD KEY `imageURL` (`imageURL`) USING BTREE,
  ADD KEY `twitterURL` (`twitterURL`) USING BTREE,
  ADD KEY `redditURL` (`redditURL`) USING BTREE,
  ADD KEY `facebookURL` (`facebookURL`) USING BTREE,
  ADD KEY `gitURL` (`gitURL`) USING BTREE;

--
-- Indexes for table `priceStats`
--
ALTER TABLE `priceStats`
  ADD PRIMARY KEY (`priceStatID`),
  ADD KEY `coinID` (`coinID`),
  ADD KEY `datetime` (`datetime`);

--
-- Indexes for table `reddit_activity`
--
ALTER TABLE `reddit_activity`
  ADD PRIMARY KEY (`activityID`),
  ADD KEY `datetime` (`datetime`),
  ADD KEY `subscribers` (`subscribers`),
  ADD KEY `activeAccounts` (`activeAccounts`),
  ADD KEY `newPosts` (`newPosts`),
  ADD KEY `subredditID` (`subredditID`),
  ADD KEY `frontpageSentiment` (`frontpageSentiment`);

--
-- Indexes for table `reddit_comments`
--
ALTER TABLE `reddit_comments`
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
-- Indexes for table `reddit_mentions`
--
ALTER TABLE `reddit_mentions`
  ADD PRIMARY KEY (`mentionID`),
  ADD KEY `mentions` (`mentions`),
  ADD KEY `topic` (`topic`),
  ADD KEY `datetime` (`date`),
  ADD KEY `sentiment` (`sentiment`);

--
-- Indexes for table `reddit_posts`
--
ALTER TABLE `reddit_posts`
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
-- Indexes for table `reddit_subreddits`
--
ALTER TABLE `reddit_subreddits`
  ADD PRIMARY KEY (`subredditID`),
  ADD KEY `name` (`name`),
  ADD KEY `topic` (`topic`);

--
-- Indexes for table `reddit_users`
--
ALTER TABLE `reddit_users`
  ADD PRIMARY KEY (`userID`),
  ADD KEY `comments` (`comments`);

--
-- Indexes for table `socialStats`
--
ALTER TABLE `socialStats`
  ADD PRIMARY KEY (`socialStatID`),
  ADD KEY `datetime` (`datetime`),
  ADD KEY `coinID` (`coinID`);

--
-- Indexes for table `twitter_mentions`
--
ALTER TABLE `twitter_mentions`
  ADD PRIMARY KEY (`mentionID`),
  ADD KEY `topic` (`topic`),
  ADD KEY `mentions` (`mentions`),
  ADD KEY `sentiment` (`sentiment`);

--
-- Indexes for table `twitter_spammers`
--
ALTER TABLE `twitter_spammers`
  ADD PRIMARY KEY (`twitterID`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `twitter_users`
--
ALTER TABLE `twitter_users`
  ADD PRIMARY KEY (`userID`),
  ADD KEY `indexed` (`indexed`),
  ADD KEY `timezone` (`timezone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth`
--
ALTER TABLE `auth`
  MODIFY `tokenID` int(8) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `coinID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `priceStats`
--
ALTER TABLE `priceStats`
  MODIFY `priceStatID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `reddit_activity`
--
ALTER TABLE `reddit_activity`
  MODIFY `activityID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `reddit_comments`
--
ALTER TABLE `reddit_comments`
  MODIFY `commentID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=180;
--
-- AUTO_INCREMENT for table `reddit_mentions`
--
ALTER TABLE `reddit_mentions`
  MODIFY `mentionID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;
--
-- AUTO_INCREMENT for table `reddit_posts`
--
ALTER TABLE `reddit_posts`
  MODIFY `postID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `reddit_subreddits`
--
ALTER TABLE `reddit_subreddits`
  MODIFY `subredditID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=191;
--
-- AUTO_INCREMENT for table `reddit_users`
--
ALTER TABLE `reddit_users`
  MODIFY `userID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;
--
-- AUTO_INCREMENT for table `socialStats`
--
ALTER TABLE `socialStats`
  MODIFY `socialStatID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `twitter_mentions`
--
ALTER TABLE `twitter_mentions`
  MODIFY `mentionID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;
--
-- AUTO_INCREMENT for table `twitter_users`
--
ALTER TABLE `twitter_users`
  MODIFY `userID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
