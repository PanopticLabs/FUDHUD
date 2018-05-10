-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 10, 2018 at 09:00 AM
-- Server version: 5.7.22-0ubuntu0.17.10.1
-- PHP Version: 7.1.15-0ubuntu0.17.10.1

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

--
-- Indexes for dumped tables
--

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
-- Indexes for table `socialStats`
--
ALTER TABLE `socialStats`
  ADD PRIMARY KEY (`socialStatID`),
  ADD KEY `datetime` (`datetime`),
  ADD KEY `coinID` (`coinID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `coinID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=222;
--
-- AUTO_INCREMENT for table `priceStats`
--
ALTER TABLE `priceStats`
  MODIFY `priceStatID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=672;
--
-- AUTO_INCREMENT for table `socialStats`
--
ALTER TABLE `socialStats`
  MODIFY `socialStatID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=695;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
