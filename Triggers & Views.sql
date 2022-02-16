--VIEWS
--Q1
CREATE VIEW IF NOT EXISTS ConstructorEmployeeOverFifty
AS
SELECT E.*, CE.CompanyName, CE.SalaryPerDay
FROM Employee E JOIN ConstructorEmployee CE
ON E.EID = CE.EID
WHERE (strftime('%Y', 'now')-strftime('%Y', E.BirthDate)) >=50;

--Q2
CREATE VIEW ApartmentNumberInNeighborhood
AS
SELECT N.NID, COUNT(*) AS ApartmentNumber
FROM Neighborhood N LEFT OUTER JOIN Apartment A
ON N.NID = A.NID
GROUP BY N.NID;

--Triggers
--Q1
CREATE TRIGGER DelEmployee
BEFORE DELETE ON Project
FOR EACH ROW
BEGIN
DELETE FROM ProjectConstructorEmployee WHERE PID = OLD.PID;
END;

CREATE TRIGGER DelEmployee1
AFTER DELETE ON ProjectConstructorEmployee
FOR EACH ROW 
BEGIN
DELETE FROM Employee WHERE EID = OLD.EID AND EID NOT IN (SELECT EID FROM ProjectConstructorEmployee GROUP BY EID);
END;


--Q2
CREATE TRIGGER MaxOfficialEmp
BEFORE INSERT ON Department
BEGIN
SELECT CASE
WHEN ((SELECT COUNT(*) 
				FROM Department
				WHERE ManagerID = new.ManagerID
				GROUP BY ManagerID) >=2)
THEN RAISE(ABORT, 'Manager can not have more then 2 Departments!')
END;
END;
