USE ElectionDB;

INSERT INTO Voter (Voter_ID, Name, Age, Gender, Constituency_ID) VALUES
(100, 'Yash', 30, 'Male', 101),
(200, 'Pradhnya', 28, 'Female', 102),
(300, 'Raju', 40, 'Male', 101),
(400, 'Sneha', 35, 'Female', 103),
(500, 'Sumit', 50, 'Male', 102);


INSERT INTO Candidate (Candidate_ID, Name, Party_ID, Status, Constituency_ID) VALUES
(1, 'Ajit Pawar', 1, 'Running', 101),
(2, 'Eknath Shinde', 2, 'Running', 102),
(3, 'Udhav Thackary', 3, 'Running', 103),
(4, 'Sangram Jagtap', 4, 'Running', 101),
(5, 'Mamta Banerjee', 5, 'Running', 103);

INSERT INTO Constituency (Constituency_ID, Name, State, Total_Votes) VALUES
(101, 'Kothrud', 'Maharashtra', 0),
(102, 'Andheri', 'Maharashtra', 0),
(103, 'Ahmednagar City', 'Maharashtra', 0),
(104, 'Buldhana', 'Maharashtra', 0),
(105, 'Satara', 'Maharashtra', 0);


INSERT INTO Voting_Centre (Centre_ID, Name, Location, Constituency_ID) VALUES
(201, 'Centre 1', 'Downtown', 101),
(202, 'Centre 2', 'Uptown', 102),
(203, 'Centre 3', 'Suburb', 103),
(204, 'Centre 4', 'Urban', 104),
(205, 'Centre 5', 'Rural', 105);


INSERT INTO Party (Party_ID, Name) VALUES
(1, 'NCP'),
(2, 'BJP'),
(3, 'Shiv Sena'),
(4, 'INC'),
(5, 'TMC');

INSERT INTO Party_Symbol (Name, Symbol) VALUES
('NCP', 'Clock'),
('BJP', 'Lotus'),
('Shiv Sena', 'Torch'),
('INC', 'Palm'),
('TMC', 'Grass');

INSERT INTO Election_Result (Result_ID, Candidate_ID, Total_Votes, Status, Constituency_ID) VALUES
(1, 1, 5000, 'Leading', 101),
(2, 2, 4500, 'Trailing', 102),
(3, 3, 5200, 'Leading', 103),
(4, 4, 4900, 'Trailing', 104),
(5, 5, 4800, 'Trailing', 105);