-- Create database
CREATE DATABASE IF NOT EXISTS lost_and_found;
USE lost_and_found;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items table
CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    status ENUM('lost','claimed','found') DEFAULT 'lost',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Claims table
CREATE TABLE claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    claimant_user_id INT NOT NULL,
    claim_message TEXT,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE,
    FOREIGN KEY (claimant_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
