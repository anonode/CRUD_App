-- Insert Customers
INSERT INTO customer (FName, LName, Address) VALUES
('J', 'Doe', '123 Maple St, Toronto, ON, Canada, M5A 1A1'),
('J', 'Smith', '456 Oak Avenue, London, England, SW1A 1AA'),
('M', 'Johnson', '789 Pine Street, Sydney, NSW, Australia, 2000'),
('S', 'Williams', '101 Birch Road, Cape Town, Western Cape, South Africa, 8001'),
('D', 'Brown', '202 Cedar Boulevard, Paris, France, 75001'),
('E', 'Jones', '303 Elm Crescent, New York, NY, USA, 10001'),
('W', 'Garcia', '404 Walnut Drive, Madrid, Spain, 28001'),
('M', 'Martinez', '505 Ash Court, Buenos Aires, Argentina, C1406'),
('J', 'Miller', '606 Pinewood Street, Tokyo, Japan, 100-0001'),
('S', 'Davis', '707 Oakwood Lane, Berlin, Germany, 10115'),
('B', 'Rodriguez', '808 Birch Avenue, Mexico City, Mexico, 01000'),
('O', 'Lee', '909 Maplewood Drive, Seoul, South Korea, 03000'),
('L', 'Hernandez', '1010 Cedar Grove, Buenos Aires, Argentina, C1407'),
('C', 'Lopez', '1111 Elmwood Lane, Rome, Italy, 00100'),
('L', 'Gonzalez', '1212 Walnut Road, Lisbon, Portugal, 1100-001'),
('A', 'Perez', '1313 Ash Street, São Paulo, Brazil, 01000-000'),
('H', 'Taylor', '1414 Elm Terrace, Toronto, ON, Canada, M4C 1A1'),
('A', 'Anderson', '1515 Pine Grove, Los Angeles, CA, USA, 90001'),
('E', 'Thomas', '1616 Oak Boulevard, Hong Kong, China, 999077');

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

-- Insert Publications
INSERT INTO publications (PubName, PubType, Frequency) VALUES
('Time Magazine', 'Magazine', 'weekly'),
('National Geographic', 'Magazine', 'monthly'),
('The New York Times', 'Newspaper', 'daily'),
('The Guardian', 'Newspaper', 'daily'),
('Sports Illustrated', 'Magazine', 'monthly'),
('The Washington Post', 'Newspaper', 'weekly'),
('Forbes', 'Magazine', 'quarterly'),
('USA Today', 'Newspaper', 'daily'),
('The Wall Street Journal', 'newspaper', '5-day'),
('People Magazine', 'Magazine', 'weekly');

-- Insert Magazines
INSERT INTO magazine (NumberOfIssues, StartDate, EndDate, Price, Frequency, SubId, Customer_id) VALUES
(12, '2024-01-01', '2024-12-31', 12.00, 'monthly', 1, 1),
(24, '2024-03-01', '2025-02-28', 18.00, 'monthly', 2, 2),
(30, '2024-05-01', '2025-05-01', 16.00, 'quarterly', 3, 3),
(12, '2024-02-01', '2024-11-30', 12.00, 'weekly', 4, 4),
(24, '2024-06-01', '2025-05-31', 18.00, 'monthly', 5, 5),
(30, '2024-04-01', '2025-04-01', 16.00, 'quarterly', 6, 6),
(12, '2024-01-01', '2024-12-31', 12.00, 'monthly', 7, 7),
(24, '2024-07-01', '2025-06-30', 18.00, 'quarterly', 8, 8),
(12, '2024-03-01', '2024-12-31', 12.00, 'weekly', 9, 9),
(30, '2024-08-01', '2025-07-31', 16.00, 'monthly', 10, 10);

-- Insert Newspapers
INSERT INTO newspaper (NumberOfMonths, StartDate, EndDate, Price, Frequency, SubId, Customer_id) VALUES
(12, '2024-01-01', '2024-12-31', 80.00, 'weekly', 1, 1),
(12, '2024-02-01', '2024-12-01', 90.00, 'weekly', 2, 2),
(12, '2024-03-01', '2024-12-01', 100.00, 'weekly', 3, 3),
(6, '2024-01-01', '2024-06-30', 50.00, '7-day', 4, 4),
(6, '2024-04-01', '2024-09-30', 45.00, '5-day', 5, 5),
(6, '2024-07-01', '2024-12-31', 30.00, '2-day', 6, 6),
(6, '2024-01-01', '2024-06-30', 60.00, '7-day', 7, 7);
