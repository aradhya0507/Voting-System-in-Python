CREATE USER 'admin'@'localhost' IDENTIFIED BY 'Admin@123';
CREATE USER 'voter'@'localhost' IDENTIFIED BY 'Voter@123';

GRANT ALL PRIVILEGES ON Voter_Management.* TO 'admin'@'localhost';
GRANT SELECT ON Voter_Management.Voter TO 'voter'@'localhost';