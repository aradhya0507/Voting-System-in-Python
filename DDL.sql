CREATE DATABASE IF NOT EXISTS Voter_Management;
USE Voter_Management;

CREATE TABLE Voter (
    Voter_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Constituency_ID INT,
    FOREIGN KEY (Constituency_ID) REFERENCES Constituency(Constituency_ID) ON DELETE CASCADE
);

CREATE TABLE Candidate (
    Candidate_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Party_ID INT,
    Status VARCHAR(50),
    Constituency_ID INT,
    FOREIGN KEY (Party_ID) REFERENCES Party(Party_ID) ON DELETE CASCADE,
    FOREIGN KEY (Constituency_ID) REFERENCES Constituency(Constituency_ID) ON DELETE CASCADE
);

CREATE TABLE Constituency (
    Constituency_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    State VARCHAR(100),
    Total_Votes INT
);

CREATE TABLE Voting_Centre (
    Centre_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Location VARCHAR(255),
    Constituency_ID INT,
    FOREIGN KEY (Constituency_ID) REFERENCES Constituency(Constituency_ID) ON DELETE CASCADE
);

CREATE TABLE Party (
    Party_ID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Party_Symbol (
    Party_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Symbol VARCHAR(50),
    FOREIGN KEY (Party_ID) REFERENCES Party(Party_ID) ON DELETE CASCADE
);

CREATE TABLE Election_Result (
    Result_ID INT PRIMARY KEY,
    Candidate_ID INT,
    Total_Votes INT,
    Status VARCHAR(50),
    Constituency_ID INT,
    FOREIGN KEY (Candidate_ID) REFERENCES Candidate(Candidate_ID) ON DELETE CASCADE,
    FOREIGN KEY (Constituency_ID) REFERENCES Constituency(Constituency_ID) ON DELETE CASCADE
);