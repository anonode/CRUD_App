-- Insert customers
INSERT INTO customer (FName, LName, Address)
VALUES 
('John', 'Doe', '123 Elm Street'),
('Jane', 'Smith', '456 Oak Avenue'),
('Michael', 'Brown', '789 Maple Road'),
('Emily', 'Davis', '321 Pine Lane'),
('Chris', 'Wilson', '654 Birch Blvd'),
('Sarah', 'Johnson', '987 Cedar Street'),
('Matthew', 'Taylor', '741 Cherry Court'),
('Laura', 'White', '852 Ash Terrace'),
('Daniel', 'Harris', '369 Walnut Drive'),
('Jessica', 'Martin', '753 Spruce Lane'),
('Andrew', 'Thompson', '951 Poplar Place'),
('Sophia', 'Garcia', '159 Cypress Way'),
('Ethan', 'Martinez', '268 Fir Circle'),
('Olivia', 'Clark', '357 Palm Grove'),
('Noah', 'Rodriguez', '486 Sycamore Ave'),
('Emma', 'Lewis', '697 Magnolia Blvd'),
('Liam', 'Walker', '875 Dogwood Trail'),
('Ava', 'Hall', '984 Hickory Road'),
('Isabella', 'Allen', '123 Willow Way'),
('Mason', 'Young', '246 Redwood Street');

-- Insert publications
INSERT INTO publications (PubName, PubType)
VALUES
('Tech Today', 'Magazine'),
('Health Weekly', 'Magazine'),
('Sports Monthly', 'Magazine'),
('Cooking Quarterly', 'Magazine'),
('Fashion Weekly', 'Magazine'),
('Travel Insights', 'Magazine'),
('Business Monthly', 'Magazine'),
('Science Quarterly', 'Magazine'),
('Art Weekly', 'Magazine'),
('Gadget World', 'Magazine'),
('City Chronicle', 'Newspaper'),
('Daily Herald', 'Newspaper'),
('Weekly Observer', 'Newspaper'),
('Morning Times', 'Newspaper'),
('Weekend Review', 'Newspaper'),
('Global News', 'Newspaper'),
('Community Bulletin', 'Newspaper');

-- Insert subscriptions
INSERT INTO subscriptions (SubType, Customer_id)
VALUES
('Magazine', 1),
('Newspaper', 1),
('Magazine', 2),
('Newspaper', 2),
('Magazine', 3),
('Newspaper', 3),
('Magazine', 4),
('Newspaper', 4),
('Magazine', 5),
('Newspaper', 5),
('Magazine', 6),
('Newspaper', 6),
('Magazine', 7),
('Newspaper', 7),
('Magazine', 8),
('Newspaper', 8),
('Magazine', 9),
('Newspaper', 9),
('Magazine', 10);

-- Insert magazine subscriptions
INSERT INTO magazine (NumberOfIssues, StartDate, SubId, Customer_id)
VALUES
('12', '2024-01-01', 1, 1),
('4', '2024-01-01', 3, 2),
('24', '2024-02-01', 5, 3),
('12', '2024-03-01', 7, 4),
('4', '2024-01-01', 9, 5),
('12', '2024-02-15', 11, 6),
('4', '2024-03-01', 13, 7),
('24', '2024-01-01', 15, 8),
('12', '2024-02-10', 17, 9),
('4', '2024-03-01', 19, 10);

-- Insert newspaper subscriptions
INSERT INTO newspaper (NumberOfMonths, StartDate, SubId, Customer_id)
VALUES
(3, '2024-01-01', 2, 1),
(6, '2024-01-15', 4, 2),
(12, '2024-02-01', 6, 3),
(3, '2024-03-01', 8, 4),
(6, '2024-01-01', 10, 5),
(12, '2024-02-01', 12, 6),
(3, '2024-03-15', 14, 7),
(6, '2024-01-01', 16, 8),
(12, '2024-02-05', 18, 9),
(3, '2024-03-01', 20, 10);
