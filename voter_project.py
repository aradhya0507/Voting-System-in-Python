import mysql.connector
from mysql.connector import Error

# Database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "voter_management"


def create_connection(database=None):
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database,
            autocommit=True
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created.")
    except Error as e:
        print(f"Error creating database: {e}")

def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Constituency (
                ConstituencyID VARCHAR(255) PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                State VARCHAR(255),
                TotalVotes INT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Voter (
                VoterID VARCHAR(255) PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Age INT,
                Gender VARCHAR(50),
                ConstituencyID VARCHAR(255),
                HasVoted BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (ConstituencyID) REFERENCES Constituency(ConstituencyID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Party (
                PartyID VARCHAR(255) PRIMARY KEY,
                Name VARCHAR(255),
                Symbol VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Candidate (
                CandidateID VARCHAR(255) PRIMARY KEY,
                Name VARCHAR(255),
                PartyID VARCHAR(255),
                ConstituencyID VARCHAR(255),
                Status VARCHAR(50),
                FOREIGN KEY (PartyID) REFERENCES Party(PartyID),
                FOREIGN KEY (ConstituencyID) REFERENCES Constituency(ConstituencyID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Election_Result (
                Result_ID INT AUTO_INCREMENT PRIMARY KEY,
                Candidate_ID VARCHAR(255),
                Constituency_ID VARCHAR(255),
                Total_Votes INT DEFAULT 0,
                Status VARCHAR(50),
                FOREIGN KEY (Candidate_ID) REFERENCES Candidate(CandidateID),
                FOREIGN KEY (Constituency_ID) REFERENCES Constituency(ConstituencyID)
            );
        """)
        print("Tables created successfully.")
    except Error as e:
        print(f"Error creating tables: {e}")

def seed_initial_data(connection):
    try:
        cursor = connection.cursor()
        # Seed parties
        parties = [
            ("BJP", "Bharatiya Janata Party", "Lotus"),
            ("CPI", "Communist Party of India", "Hammer and Sickle"),
            ("INC", "Indian National Congress", "Hand")
        ]
        cursor.executemany("INSERT IGNORE INTO Party (PartyID, Name, Symbol) VALUES (%s, %s, %s)", parties)

        # Seed constituencies
        constituencies = [(str(i), f"Constituency {i}", "State X", 0) for i in range(1, 11)]
        cursor.executemany("INSERT IGNORE INTO Constituency (ConstituencyID, Name, State, TotalVotes) VALUES (%s, %s, %s, %s)", constituencies)
        print("Initial data seeded successfully.")
    except Error as e:
        print(f"Error seeding data: {e}")

def view_results(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        constituency_id = input("Enter Constituency ID to view results: ")
        cursor.execute("""
            SELECT c.CandidateID, c.Name AS CandidateName, p.Name AS PartyName, er.Total_Votes
            FROM Candidate c
            JOIN Party p ON c.PartyID = p.PartyID
            JOIN Election_Result er ON c.CandidateID = er.Candidate_ID
            WHERE c.ConstituencyID = %s;
        """, (constituency_id,))
        results = cursor.fetchall()
        if results:
            print("\n--- Election Results ---")
            for row in results:
                print(f"Candidate: {row['CandidateName']} ({row['PartyName']}), Votes: {row['Total_Votes']}")
        else:
            print("No results available for this constituency.")
    except Error as e:
        print(f"Error retrieving results: {e}")

def cast_vote(connection):
    try:
        cursor = connection.cursor()
        voter_id = input("Enter your Voter ID: ")
        cursor.execute("SELECT HasVoted, ConstituencyID FROM Voter WHERE VoterID = %s", (voter_id,))
        voter = cursor.fetchone()
        if not voter:
            print("Voter ID not found.")
            return
        if voter[0]:
            print("You have already voted.")
            return

        constituency_id = voter[1]
        cursor.execute("SELECT CandidateID, Name FROM Candidate WHERE ConstituencyID = %s", (constituency_id,))
        candidates = cursor.fetchall()
        if not candidates:
            print("No candidates available to vote for.")
            return

        print("Candidates:")
        for i, (cid, name) in enumerate(candidates, 1):
            print(f"{i}. {name} ({cid})")

        choice = int(input("Enter the number of the candidate you want to vote for: "))
        selected_candidate = candidates[choice - 1][0]

        cursor.execute("""
            UPDATE Election_Result
            SET Total_Votes = Total_Votes + 1
            WHERE Candidate_ID = %s AND Constituency_ID = %s
        """, (selected_candidate, constituency_id))
        cursor.execute("UPDATE Voter SET HasVoted = TRUE WHERE VoterID = %s", (voter_id,))
        print("Vote cast successfully.")
    except Error as e:
        print(f"Error casting vote: {e}")

def add_voter(connection):
    try:
        cursor = connection.cursor()
        voter_id = input("Enter Voter ID: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")
        gender = input("Enter Gender: ")
        constituency_id = input("Enter Constituency ID: ")
        
        # Verify constituency exists
        cursor.execute("SELECT COUNT(*) FROM Constituency WHERE ConstituencyID = %s", (constituency_id,))
        if cursor.fetchone()[0] == 0:
            print("Error: Constituency ID does not exist.")
            return
        
        cursor.execute("""
            INSERT INTO Voter (VoterID, Name, Age, Gender, ConstituencyID, HasVoted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (voter_id, name, age, gender, constituency_id))
        print("Voter added successfully.")
    except Error as e:
        print(f"Error adding voter: {e}")

def view_voter(connection):
    try:
        cursor = connection.cursor()
        voter_id = input("Enter Voter ID to view (leave blank to view all): ")
        if voter_id:
            cursor.execute("""
                SELECT v.VoterID, v.Name, v.Age, v.Gender, v.HasVoted, c.Name as Constituency
                FROM Voter v
                JOIN Constituency c ON v.ConstituencyID = c.ConstituencyID
                WHERE v.VoterID = %s
            """, (voter_id,))
            voter = cursor.fetchone()
            if voter:
                print("\n--- Voter Details ---")
                print(f"ID: {voter[0]}")
                print(f"Name: {voter[1]}")
                print(f"Age: {voter[2]}")
                print(f"Gender: {voter[3]}")
                print(f"Has Voted: {'Yes' if voter[4] else 'No'}")
                print(f"Constituency: {voter[5]}")
            else:
                print("Voter not found.")
        else:
            cursor.execute("""
                SELECT v.VoterID, v.Name, v.Age, v.Gender, v.HasVoted, c.Name as Constituency
                FROM Voter v
                JOIN Constituency c ON v.ConstituencyID = c.ConstituencyID
            """)
            voters = cursor.fetchall()
            if voters:
                print("\n--- All Voters ---")
                for voter in voters:
                    print(f"ID: {voter[0]}, Name: {voter[1]}, Age: {voter[2]}, Gender: {voter[3]}, Has Voted: {'Yes' if voter[4] else 'No'}, Constituency: {voter[5]}")
            else:
                print("No voters found.")
    except Error as e:
        print(f"Error viewing voter: {e}")

def update_voter(connection):
    try:
        cursor = connection.cursor()
        voter_id = input("Enter Voter ID to update: ")
        
        # Check if voter exists
        cursor.execute("SELECT COUNT(*) FROM Voter WHERE VoterID = %s", (voter_id,))
        if cursor.fetchone()[0] == 0:
            print("Voter not found.")
            return
        
        print("Leave blank for no change:")
        name = input("Enter new Name: ")
        age = input("Enter new Age: ")
        gender = input("Enter new Gender: ")
        constituency_id = input("Enter new Constituency ID: ")
        
        # Build update query dynamically
        query = "UPDATE Voter SET "
        params = []
        updates = []
        
        if name:
            updates.append("Name = %s")
            params.append(name)
        if age:
            updates.append("Age = %s")
            params.append(age)
        if gender:
            updates.append("Gender = %s")
            params.append(gender)
        if constituency_id:
            # Verify constituency exists
            cursor.execute("SELECT COUNT(*) FROM Constituency WHERE ConstituencyID = %s", (constituency_id,))
            if cursor.fetchone()[0] == 0:
                print("Error: Constituency ID does not exist.")
                return
            updates.append("ConstituencyID = %s")
            params.append(constituency_id)
        
        if not updates:
            print("No updates provided.")
            return
            
        query += ", ".join(updates)
        query += " WHERE VoterID = %s"
        params.append(voter_id)
        
        cursor.execute(query, params)
        print("Voter updated successfully.")
    except Error as e:
        print(f"Error updating voter: {e}")

def delete_voter(connection):
    try:
        cursor = connection.cursor()
        voter_id = input("Enter Voter ID to delete: ")
        
        # Check if voter exists
        cursor.execute("SELECT COUNT(*) FROM Voter WHERE VoterID = %s", (voter_id,))
        if cursor.fetchone()[0] == 0:
            print("Voter not found.")
            return
            
        confirm = input(f"Are you sure you want to delete voter {voter_id}? (y/n): ")
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM Voter WHERE VoterID = %s", (voter_id,))
            print("Voter deleted successfully.")
        else:
            print("Deletion cancelled.")
    except Error as e:
        print(f"Error deleting voter: {e}")

def drop_database():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            confirm = input(f"Are you sure you want to drop the database '{DB_NAME}'? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
                print(f"Database '{DB_NAME}' dropped successfully.")
            else:
                print("Operation cancelled.")
            connection.close()
    except Error as e:
        print(f"Error dropping database: {e}")

def manage_parties(connection):
    try:
        cursor = connection.cursor()
        print("\n--- Manage Parties ---")
        print("1. View Parties")
        print("2. Add Party")
        print("3. Update Party")
        print("4. Delete Party")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            cursor.execute("SELECT * FROM Party")
            parties = cursor.fetchall()
            if parties:
                print("\n--- All Parties ---")
                for party in parties:
                    print(f"ID: {party[0]}, Name: {party[1]}, Symbol: {party[2]}")
            else:
                print("No parties found.")
                
        elif choice == '2':
            party_id = input("Enter Party ID: ")
            name = input("Enter Party Name: ")
            symbol = input("Enter Party Symbol: ")
            cursor.execute("INSERT INTO Party (PartyID, Name, Symbol) VALUES (%s, %s, %s)", 
                          (party_id, name, symbol))
            print("Party added successfully.")
            
        elif choice == '3':
            party_id = input("Enter Party ID to update: ")
            cursor.execute("SELECT COUNT(*) FROM Party WHERE PartyID = %s", (party_id,))
            if cursor.fetchone()[0] == 0:
                print("Party not found.")
                return
                
            print("Leave blank for no change:")
            name = input("Enter new Party Name: ")
            symbol = input("Enter new Party Symbol: ")
            
            query = "UPDATE Party SET "
            params = []
            updates = []
            
            if name:
                updates.append("Name = %s")
                params.append(name)
            if symbol:
                updates.append("Symbol = %s")
                params.append(symbol)
                
            if not updates:
                print("No updates provided.")
                return
                
            query += ", ".join(updates)
            query += " WHERE PartyID = %s"
            params.append(party_id)
            
            cursor.execute(query, params)
            print("Party updated successfully.")
            
        elif choice == '4':
            party_id = input("Enter Party ID to delete: ")
            cursor.execute("SELECT COUNT(*) FROM Party WHERE PartyID = %s", (party_id,))
            if cursor.fetchone()[0] == 0:
                print("Party not found.")
                return
                
            # Check if party is used by any candidates
            cursor.execute("SELECT COUNT(*) FROM Candidate WHERE PartyID = %s", (party_id,))
            if cursor.fetchone()[0] > 0:
                print("Cannot delete party: It is associated with candidates.")
                return
                
            confirm = input(f"Are you sure you want to delete party {party_id}? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM Party WHERE PartyID = %s", (party_id,))
                print("Party deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice.")
    except Error as e:
        print(f"Error managing parties: {e}")

def manage_constituencies(connection):
    try:
        cursor = connection.cursor()
        print("\n--- Manage Constituencies ---")
        print("1. View Constituencies")
        print("2. Add Constituency")
        print("3. Update Constituency")
        print("4. Delete Constituency")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            cursor.execute("SELECT * FROM Constituency")
            constituencies = cursor.fetchall()
            if constituencies:
                print("\n--- All Constituencies ---")
                for constituency in constituencies:
                    print(f"ID: {constituency[0]}, Name: {constituency[1]}, State: {constituency[2]}, Total Votes: {constituency[3]}")
            else:
                print("No constituencies found.")
                
        elif choice == '2':
            constituency_id = int(input("Enter Constituency ID: "))
            name = input("Enter Constituency Name: ")
            state = input("Enter State: ")
            total_votes = input("Enter Total Votes (default 0): ") or "0"
            
            cursor.execute("""
                INSERT INTO Constituency (ConstituencyID, Name, State, TotalVotes)
                VALUES (%i, %s, %s, %s)
            """, (constituency_id, name, state, total_votes))
            print("Constituency added successfully.")
            
        elif choice == '3':
            constituency_id = input("Enter Constituency ID to update: ")
            cursor.execute("SELECT COUNT(*) FROM Constituency WHERE ConstituencyID = %s", (constituency_id,))
            if cursor.fetchone()[0] == 0:
                print("Constituency not found.")
                return
                
            print("Leave blank for no change:")
            name = input("Enter new Constituency Name: ")
            state = input("Enter new State: ")
            total_votes = input("Enter new Total Votes: ")
            
            query = "UPDATE Constituency SET "
            params = []
            updates = []
            
            if name:
                updates.append("Name = %s")
                params.append(name)
            if state:
                updates.append("State = %s")
                params.append(state)
            if total_votes:
                updates.append("TotalVotes = %s")
                params.append(total_votes)
                
            if not updates:
                print("No updates provided.")
                return
                
            query += ", ".join(updates)
            query += " WHERE ConstituencyID = %s"
            params.append(constituency_id)
            
            cursor.execute(query, params)
            print("Constituency updated successfully.")
            
        elif choice == '4':
            constituency_id = input("Enter Constituency ID to delete: ")
            cursor.execute("SELECT COUNT(*) FROM Constituency WHERE ConstituencyID = %s", (constituency_id,))
            if cursor.fetchone()[0] == 0:
                print("Constituency not found.")
                return
                
            # Check if constituency is used by voters or candidates
            cursor.execute("SELECT COUNT(*) FROM Voter WHERE ConstituencyID = %s", (constituency_id,))
            has_voters = cursor.fetchone()[0] > 0
            
            cursor.execute("SELECT COUNT(*) FROM Candidate WHERE ConstituencyID = %s", (constituency_id,))
            has_candidates = cursor.fetchone()[0] > 0
            
            if has_voters or has_candidates:
                print("Cannot delete constituency: It is associated with voters or candidates.")
                return
                
            confirm = input(f"Are you sure you want to delete constituency {constituency_id}? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM Constituency WHERE ConstituencyID = %s", (constituency_id,))
                print("Constituency deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice.")
    except Error as e:
        print(f"Error managing constituencies: {e}")

def voter_menu(connection):
    while True:
        print("\n--- Voter Management System ---")
        print("1. View Voter")
        print("2. Exit")
        print("3. View Constituency Election Results")
        print("4. Cast Vote")

        choice = input("Enter your choice: ")
        if choice == '1': view_voter(connection)
        elif choice == '2': break
        elif choice == '3': view_results(connection)
        elif choice == '4': cast_vote(connection)
        else: print("Invalid choice. Please try again.")

def manage_candidates(connection):
    try:
        cursor = connection.cursor()
        print("\n--- Manage Candidates ---")
        print("1. View Candidates")
        print("2. Add Candidate")
        print("3. Delete Candidate")
        choice = input("Enter your choice: ")
        if choice == '1':
            cursor.execute("""
                SELECT c.CandidateID, c.Name, p.Name as PartyName, c.ConstituencyID, c.Status
                FROM Candidate c
                JOIN Party p ON c.PartyID = p.PartyID
            """)
            candidates = cursor.fetchall()
            if candidates:
                print("\n--- All Candidates ---")
                for candidate in candidates:
                    print(f"ID: {candidate[0]}, Name: {candidate[1]}, Party: {candidate[2]}, Constituency: {candidate[3]}, Status: {candidate[4]}")
            else:
                print("No candidates found.")
        elif choice == '2':
            cid = input("Enter Candidate ID: ")
            name = input("Enter Name: ")
            party_id = input("Enter Party ID: ")
            constituency_id = input("Enter Constituency ID: ")
            status = input("Enter Status: ")
            cursor.execute("INSERT INTO Candidate (CandidateID, Name, PartyID, ConstituencyID, Status) VALUES (%s, %s, %s, %s, %s)", (cid, name, party_id, constituency_id, status))
            cursor.execute("INSERT INTO Election_Result (Candidate_ID, Constituency_ID, Status) VALUES (%s, %s, %s)", (cid, constituency_id, status))
            print("Candidate added.")
        elif choice == '3':
            cid = input("Enter Candidate ID to delete: ")
            # Check if candidate exists
            cursor.execute("SELECT COUNT(*) FROM Candidate WHERE CandidateID = %s", (cid,))
            if cursor.fetchone()[0] == 0:
                print("Candidate not found.")
                return
                
            confirm = input(f"Are you sure you want to delete candidate {cid}? (y/n): ")
            if confirm.lower() == 'y':
                # First delete from Election_Result due to foreign key constraint
                cursor.execute("DELETE FROM Election_Result WHERE Candidate_ID = %s", (cid,))
                cursor.execute("DELETE FROM Candidate WHERE CandidateID = %s", (cid,))
                print("Candidate deleted.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice.")
    except Error as e:
        print(f"Error managing candidates: {e}")

def admin_menu(connection):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Voter")
        print("2. View Voter")
        print("3. Update Voter")
        print("4. Delete Voter")
        print("5. Drop Database")
        print("6. Exit")
        print("7. View Constituency Election Results")
        print("8. Manage Parties")
        print("9. Manage Constituencies")
        print("10. Manage Candidates")

        choice = input("Enter your choice: ")
        if choice == '1': add_voter(connection)
        elif choice == '2': view_voter(connection)
        elif choice == '3': update_voter(connection)
        elif choice == '4': delete_voter(connection)
        elif choice == '5': drop_database(); break
        elif choice == '6': break
        elif choice == '7': view_results(connection)
        elif choice == '8': manage_parties(connection)
        elif choice == '9': manage_constituencies(connection)
        elif choice == '10': manage_candidates(connection)
        else: print("Invalid choice. Please try again.")


connection = create_connection()
if connection:
    create_database(connection)
    connection.close()

    connection = create_connection(DB_NAME)
    if connection:
        create_tables(connection)
        seed_initial_data(connection)
        while True:
            print("\n--- Voter Management System ---")
            print("1. Admin")
            print("2. Voter")
            print("3. Exit")
            choice = input("Enter user type: ")
            if choice == '1': admin_menu(connection)
            elif choice == '2': voter_menu(connection)
            elif choice == '3': break
            else: print("Invalid choice.")
            connection.close()
    else:
        print("Failed to connect to the database.")

