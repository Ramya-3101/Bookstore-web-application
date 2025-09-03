-- Create Database
CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- Create Books Table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    price DECIMAL(10,2),
    stock INT
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    book_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Insert Sample Books
INSERT INTO books (title, author, price, stock) VALUES
('Pride and Prejudice', 'Jane Austen', 299.00, 15),
('To Kill a Mockingbird', 'Harper Lee', 349.00, 12),
('1984', 'George Orwell', 399.00, 10),
('The Great Gatsby', 'F. Scott Fitzgerald', 279.00, 8),
('The Catcher in the Rye', 'J.D. Salinger', 319.00, 7),
('Moby Dick', 'Herman Melville', 459.00, 6),
('War and Peace', 'Leo Tolstoy', 699.00, 5),
('The Alchemist', 'Paulo Coelho', 249.00, 20),
('The Hobbit', 'J.R.R. Tolkien', 499.00, 10),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 599.00, 18);
